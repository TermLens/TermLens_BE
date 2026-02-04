import json
import hashlib
from trafilatura import extract
import boto3

from llm_client import LLMClient
from text_splitter import split_sentences_block
from tos_evaluate import evaluate_category_summaries
from tos_processing import categorize_sentences, score_sentence_importance
from tos_summarize import summarize_by_category

def lambda_handler(event, context):
    # url이 없거나 빈 문자열인 경우
    if ('queryStringParameters' not in event
        or 'url' not in event['queryStringParameters']
        or not event['queryStringParameters']['url']):

        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'url 파라미터가 필요합니다.'
            }, ensure_ascii=False)
        }

    # body가 없거나 빈 문자열인 경우
    if 'body' not in event or not event['body']:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': '분석할 약관이 없습니다.'
            }, ensure_ascii=False)
        }

    url = event['queryStringParameters']['url']
    tos_content = extract(event['body'], output_format='html')

    if not tos_content:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': '약관 전처리에 실패했습니다.'
            }, ensure_ascii=False)
        }

    # 바이트 기준으로 길이 및 감소율 계산
    original_length = len(event['body'].encode('utf-8'))
    processed_length = len(tos_content.encode('utf-8'))
    
    print(f"원본 html 길이: {original_length} bytes")
    print(f"trafilatura 전처리 후 길이: {processed_length} bytes")

    # url에서 쿼리 파라미터(?), 해시(#) 제거
    url = url.split('?')[0].split('#')[0]
    # URL 해시: DynamoDB 조회용 키
    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
    # 콘텐츠 해시: 페이지 본문 변경 여부 확인용
    content_hash = hashlib.sha256(tos_content.encode('utf-8')).hexdigest()

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('termlens-tos-analysis')

    # DynamoDB에서 URL 해시로 기존 분석 결과 조회
    db_response = table.get_item(Key={'url': url_hash})

    # 기존 분석 결과가 있고, 콘텐츠 해시가 일치하면 캐시 반환
    if 'Item' in db_response and db_response['Item'].get('content_hash') == content_hash:
        evaluation_result = db_response['Item']
        print("캐시 존재, 이전 분석 결과 반환")
        return {
            'statusCode': 200,
            'body': json.dumps({
                "overall_evaluation": evaluation_result.get("overall_evaluation"),
                "evaluation_for_each_clause": evaluation_result.get("evaluation_for_each_clause")
            }, ensure_ascii=False)
        }

    # 캐시가 없거나 콘텐츠가 변경된 경우 새로 분석
    if 'Item' in db_response:
        print("캐시 내용 불일치, 새로 분석")
    else:
        print("캐시 없음, 새로 분석")

    client = LLMClient(temperature=0)

    # 1) 문장 단위 분할
    sentences = split_sentences_block(tos_content, client)
    print(f"문장 분할 개수: {len(sentences)}")
    print(f"문장들 길이 합: {sum(len(s) for s in sentences)}")

    # 1-1) 짧은 문장 필터링 (10자 이하 제거)
    sentences = [s for s in sentences if len(s) > 10]
    print(f"10자 이하 제거 후 문장 개수: {len(sentences)}")

    # 2) 중요도 점수화
    scored_sentences = score_sentence_importance(sentences, client)
    # 중요도 결과에 원문 문장 재결합 (모델 출력에 sentence 포함 안 함)
    index_to_sentence = {idx: sentences[idx].strip() for idx in range(len(sentences))}
    for item in scored_sentences:
        idx = item.get("id")
        if idx in index_to_sentence:
            item["sentence"] = index_to_sentence[idx]

    important_sentences = [
        item for item in scored_sentences if item.get("importance_score", 0) >= 4
    ]
    print(f"중요도 4 이상 문장 수: {len(important_sentences)}")
    print(f"중요도 4 이상 문장들 길이 합: {sum(len(item.get('sentence', '')) for item in important_sentences)}")

    # 3) 카테고리 분류
    categorize_input = [
        {"id": item.get("id"), "sentence": item.get("sentence", "")}
        for item in important_sentences
    ]
    categorized_raw = categorize_sentences(categorize_input, client)
    index_to_important = {item.get("id"): item for item in important_sentences}
    categorized = []
    for item in categorized_raw:
        idx = item.get("id")
        base = index_to_important.get(idx)
        if base:
            categorized.append({**base, "category": item.get("category", "기타")})

    # 카테고리별 문장 수 계산 후 출력 (디버깅 용도)
    category_counts = {}
    for item in categorized:
        category = item.get("category", "UNKNOWN")
        category_counts[category] = category_counts.get(category, 0) + 1
    print("카테고리별 문장 수:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")

    # 4) 카테고리별 요약
    category_summaries = summarize_by_category(categorized, client)

    # 5) 요약 평가
    evaluation_result = evaluate_category_summaries(category_summaries, client)

    # DynamoDB에 분석 결과와 콘텐츠 해시 저장
    table.put_item(Item={
        'url': url_hash,
        'content_hash': content_hash,
        'overall_evaluation': evaluation_result.get("overall_evaluation"),
        'evaluation_for_each_clause': evaluation_result.get("evaluation_for_each_clause")
    })

    return {
        'statusCode': 200,
        'body': json.dumps({
            "overall_evaluation": evaluation_result.get("overall_evaluation"),
            "evaluation_for_each_clause": evaluation_result.get("evaluation_for_each_clause")
        }, ensure_ascii=False)
    }

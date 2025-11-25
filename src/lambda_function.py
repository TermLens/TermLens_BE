import json
from trafilatura import extract

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
    markdown_length = len(tos_content.encode('utf-8'))
    reduction = (original_length - markdown_length) / original_length * 100
    
    print(f"원본 html 길이: {original_length} bytes")
    print(f"markdown 길이: {markdown_length} bytes")
    print(f"감소율: {reduction:.2f}%")

    # TODO: 기존 URL 기반 캐싱 로직 구현

    client = LLMClient()

    # 1) 문장 단위 분할
    sentences = split_sentences_block(tos_content)
    print(f"문장 분할 개수: {len(sentences)}")

    # 2) 중요도 점수화
    scored_sentences = score_sentence_importance(sentences, client)
    important_sentences = [
        item for item in scored_sentences if item.get("importance_score", 0) >= 3
    ]
    print(f"중요도 3 이상 문장 수: {len(important_sentences)}")

    # 3) 카테고리 분류
    categorized = categorize_sentences(important_sentences, client)

    # 4) 카테고리별 요약
    category_summaries = summarize_by_category(categorized, client)

    # 5) 요약 평가
    evaluation_result = evaluate_category_summaries(category_summaries, client)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "url": url,
            "stats": {
                "total_sentences": len(sentences),
                "kept_sentences": len(important_sentences),
                "reduction_rate_percent": reduction
            },
            "category_results": evaluation_result
        }, ensure_ascii=False)
    }

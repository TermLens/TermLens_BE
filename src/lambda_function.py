import json
import boto3
from markdownify import markdownify as md

from tos_summarize import tos_summarize
from tos_evaluate import tos_evaluate
from llm_client import LLMClient

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
    tos_content = md(event['body'])

    # 바이트 기준으로 길이 및 감소율 계산
    original_length = len(event['body'].encode('utf-8'))
    markdown_length = len(tos_content.encode('utf-8'))
    reduction = (original_length - markdown_length) / original_length * 100
    
    print(f"원본 html 길이: {original_length} bytes")
    print(f"markdown 길이: {markdown_length} bytes")
    print(f"감소율: {reduction:.2f}%")

    # url에서 쿼리 파라미터(?), 해시(#) 제거
    url = url.split('?')[0].split('#')[0]

    s3 = boto3.client("s3")
    bucket = 'inha-capstone-20-tos-content-caching'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('inha-capstone-20-tos-analysis')
    key = url

    # try: S3에서 해당 url을 key로 갖는 객체 가져오기
    try:
        response = s3.get_object(Bucket=bucket, Key=url)
        saved_tos_content = response['Body'].read().decode('utf-8')

        # 기존 tos_content와 비교
        if saved_tos_content == tos_content:
            # 동일하면 DynamoDB에서 이전 분석 결과를 가져와 return
            db_response = table.get_item(Key={'url': url})
            if 'Item' in db_response:
                evaluation_result = db_response['Item']
                print("캐시 존재, 이전 분석 결과 반환")
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        "overall_evaluation": evaluation_result.get("overall_evaluation"),
                        "evaluation_for_each_clause": evaluation_result.get("evaluation_for_each_clause")
                    }, ensure_ascii=False)
                }
        
        # 내용이 다르면 S3 업데이트
        s3.put_object(Bucket=bucket, Key=key, Body=tos_content.encode('utf-8'))
        print("캐시 내용 불일치, 새로 저장")
    # except: 없는 경우 현재 url을 key로 tos_content 저장
    except s3.exceptions.NoSuchKey:
        s3.put_object(Bucket=bucket, Key=key, Body=tos_content.encode('utf-8'))
        print("캐시 없음, 새로 저장")

    client = LLMClient()

    # tos_content 문자열에서 중요 조항 위주로 약관 요약
    summarized_tos = tos_summarize(tos_content, client)

    # 약관 조항에 대해 분석 수행
    evaluation_result = tos_evaluate(summarized_tos, client)

    # DynamoDB에 분석 결과 저장
    table.put_item(Item={
        'url': url,
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

import json
from markdownify import markdownify as md

from tos_summarize import tos_summarize
from tos_evaluate import tos_evaluate

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
    print(f"감소율: {reduction:.4f}%")

    # TODO: 기존 URL 기반 캐싱 로직 구현

    # tos_content 문자열에서 중요 조항 위주로 약관 요약
    summarized_tos = tos_summarize(tos_content)

    # 약관 조항에 대해 분석 수행
    evaluation_result = tos_evaluate(summarized_tos)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "overall_evaluation": evaluation_result.get("overall_evaluation"),
            "evaluation_for_each_clause": evaluation_result.get("evaluation_for_each_clause")
        }, ensure_ascii=False)
    }

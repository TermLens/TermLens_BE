import json
import os
from google import genai

from tos_summarize import tos_summarize
from tos_evaluate import tos_evaluate

def lambda_handler(event, context):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

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
    text_html = event['body']

    # TODO: 기존 URL 기반 캐싱 로직 구현

    # text_html 문자열에서 중요 조항 위주로 약관 요약
    summarized_tos = tos_summarize(text_html, client)

    # 약관 조항에 대해 분석 수행
    # gemini api의 rate limit 문제로, 여러 조항을 한 번에 보내지 않고 하나씩 처리
    evaluation_result = tos_evaluate(summarized_tos, client)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "overall_evaluation": evaluation_result.get("overall_evaluation"),
            "evaluation_for_each_clause": evaluation_result.get("evaluation_for_each_clause")
        }, ensure_ascii=False)
    }

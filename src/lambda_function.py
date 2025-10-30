import json
import os
from google import genai

def lambda_handler(event, context):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
    model="gemini-2.5-flash-lite", contents="hello to me!"
    )

    url = event['queryStringParameters']['url']
    text_html = event['queryStringParameters']['body']

    # TODO: 기존 URL 기반 캐싱 로직 구현

    # TODO: text_html 문자열에서 중요 조항 위주로 약관 요약

    # TODO: 각 요약된 조항에 대해 분석 수행

    return {
        'statusCode': 200,
        'body': json.dumps(response.text)
    }

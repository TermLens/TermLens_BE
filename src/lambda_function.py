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
    text_html = event['body']

    # TODO: 기존 URL 기반 캐싱 로직 구현

    # TODO: text_html 문자열에서 중요 조항 위주로 약관 요약

    # TODO: 각 요약된 조항에 대해 분석 수행

    return {
        'statusCode': 200,
        'body': json.dumps({
            "overall_evaluation": "E",
            "evaluation_for_each_clause": [
                {
                    "evaluation": "neutral",
                    "summarized_clause": "이용자는 본 약관에 동의함으로써 당 서비스를 이용할 수 있습니다."
                },
                {
                    "evaluation": "neutral",
                    "summarized_clause": "당 회사는 이용자의 개인정보를 보호하기 위해 최선을 다합니다."
                },
                {
                    "evaluation": "bad",
                    "summarized_clause": "서비스 이용 중 발생하는 문제에 대해 당 회사는 책임을 지지 않습니다."
                }
            ]
        }, ensure_ascii=False)
    }

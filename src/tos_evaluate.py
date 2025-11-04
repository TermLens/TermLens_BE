import enum
import json
from google import genai
from google.genai import types

def tos_evaluate(summarized_tos, client):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=
            """
            당신은 약관 분석 전문가입니다. 주어진 약관 및 각 조항을 평가합니다.
            각 약관 조항은 good, neutral, bad 중 하나로 평가합니다.
            'good'은 이용자에게 유리한 조항, 'neutral'은 중립적인 조항, 'bad'는 이용자에게 불리한 조항을 의미합니다.
            A, B, C, D, E 등급 중 하나로 전체 약관을 평가합니다.
            A는 매우 우수한 약관, E는 매우 불리한 약관을 의미합니다.
            한국어로 응답합니다.
            """,
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "overall_evaluation": {
                        "type": "string"
                    },
                    "evaluation_for_each_clause": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "evaluation": {
                                    "type": "string"
                                },
                                "summarized_clause": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                }
            }
        ),
        contents=summarized_tos,
    )

    # response에서 JSON 파싱 후 반환

    return json.loads(response.text)

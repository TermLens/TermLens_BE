import json
import boto3

def tos_evaluate(summarized_tos):
    client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2"
)

    model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    messages = [{
        "role": "user",
        "content": [{"text": summarized_tos}]
        }]

    response = client.converse(
        modelId=model_id,
        system="""
당신은 약관 분석 전문가입니다. 주어진 약관 및 각 조항을 평가합니다.
각 약관 조항은 good, neutral, bad 중 하나로 평가합니다.
'good'은 이용자에게 유리한 조항, 'neutral'은 중립적인 조항, 'bad'는 이용자에게 불리한 조항을 의미합니다.
A, B, C, D, E 등급 중 하나로 전체 약관을 평가합니다.
A는 매우 우수한 약관, E는 매우 불리한 약관을 의미합니다.
한국어로 응답합니다.
아래의 JSON 양식으로 응답합니다:
{
    "overall_evaluation": "D",
    "evaluation_for_each_clause": [
        {
            "evaluation": "neutral",
            "summarized_clause": "AWS 사이트 콘텐츠의 저작권은 AWS 또는 제공자에게 있으며, 관련 법률에 의해 보호됨을 명시합니다."
        },
        {
            "evaluation": "neutral",
            "summarized_clause": "AWS 상표 및 트레이드 드레스는 허가 없이 사용할 수 없으며, 타사 상표는 해당 소유자에게 있음을 명시합니다."
        },
        {
            "evaluation": "bad",
            "summarized_clause": "개인적인 사이트 이용 목적 외 상업적 재판매, 복제, 변경 등은 사전 서면 동의 없이는 금지됨을 명시하며, 이는 일반적인 내용이나 명확한 제한을 둠."
        },
        {
            "evaluation": "bad",
            "summarized_clause": "이용자의 계정 및 비밀번호 관리 책임을 명시하고, 계정 활동에 대한 책임을 이용자에게 부과합니다. 또한 AWS는 일방적으로 서비스 거절 및 계정 해지 권한을 가집니다."
        }
    ]
}
""",
        messages=messages,
    )

    print("TOS Evaluation Response:")
    print(response)

    # response에서 JSON 파싱 후 반환
    return json.loads(response['output']['message']['content'][0]['text'])

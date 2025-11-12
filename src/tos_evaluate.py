import json
import boto3

def tos_evaluate(summarized_tos):
    system_instruction=[{"text": """
당신은 전문적인 약관 분석 AI입니다. 주어진 약관 내용 및 각 조항을 평가합니다.
주어진 약관은 주요 조항을 위주로 요약된 내용입니다.
JSON 양식으로, 다음의 key값을 사용합니다.
"overall_evaluation": "A|B|C|D|E",
"evaluation_for_each_clause": [
    "evaluation": "good|neutral|bad",
    "summarized_clause": "조항 요약 내용"
]
"overall_evaluation"은 전체 약관의 등급을 나타냅니다. A는 가장 우수한 약관, E는 가장 불리한 약관입니다.
"evaluation_for_each_clause"는 각 조항에 대한 평가를 포함하는 리스트입니다.
"evaluation"은 각 조항이 소비자에게 유리한지(good)/중립적인지(neutral)/불리한지(bad)를 나타냅니다.
"summarized_clause"는 각 조항의 요약된 내용을 포함합니다.
JSON 형식 이외에 서론이나 결론, 코드 블럭 따위는 절대로 포함하지 마십시오.
응답은 곧바로 json.loads()를 통해 파싱되기 때문에 반드시 여는 중괄호(`{`})로 시작하고 닫는 중괄호(`}`)로 끝나야 합니다.
예시 응답:
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
"""}]
    client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2"
)

    model_id = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    messages = [{
        "role": "user",
        "content": [
            {"text": summarized_tos}
        ]
    }]

    response = client.converse(
        modelId=model_id,
        system=system_instruction,
        messages=messages,
    )

    print("TOS Evaluation Response:")
    print(response)

    text = response['output']['message']['content'][0]['text']
    start = text.find('{')
    end = text.rfind('}') + 1
    json_text = text[start:end]

    # response에서 JSON 파싱 후 반환
    return json.loads(json_text)
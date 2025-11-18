import json
import boto3

SYSTEM_PROMPT_TOS_EVALUATE = """
당신은 약관 분석 전문 AI입니다. 당신의 임무는 주어진 요약된 약관 조항들을 평가하여
소비자 관점에서 good / neutral / bad 라벨을 부여하고 전체적인 등급을 산정하는 것입니다.

반드시 다음 규칙을 지키십시오:

1. JSON 형식만 출력하십시오.
2. JSON 이외의 설명, 서론, 결론, 코드블록은 절대 포함하지 마십시오.
3. 출력 형식은 아래 스키마를 정확히 따라야 합니다:

{
    "overall_evaluation": "A|B|C|D|E",
    "evaluation_for_each_clause": [
        {
            "evaluation": "good|neutral|bad",
            "summarized_clause": "요약된 조항 내용 그대로",
            "reason": "라벨을 판단한 짧은 이유 (1~2 문장)"
        }
    ]
}

4. 평가 기준:
- good: 이용자에게 명확한 이익·보호 장치가 존재할 때
- neutral: 일반적인 법적·운영적 조항으로 특별히 불리함이 없을 때
- bad: 책임 제한, 과도한 서비스 권한, 불리한 이용자 의무, 일방적 변경 가능성 등

5. 전체 등급(overall_evaluation) 기준:
- bad가 매우 많으면 E
- bad가 많으면 D
- neutral 위주면 C
- good과 neutral 섞이면 B
- good이 많고 bad 거의 없으면 A

당신의 응답은 무조건 하나의 JSON 객체여야 하며, 곧바로 json.loads()로 파싱될 수 있어야 합니다.
"""

def count_score(eval_list):
    scores = [item["evaluation"] for item in eval_list]
    
    bad = scores.count("bad")
    good = scores.count("good")

    if bad >= 5:
        return "E"
    if bad >= 3:
        return "D"
    if bad >= 1:
        return "C"
    if good >= 7:
        return "A"
    
    return "B"

def tos_evaluate(summarized_list):
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2"
    )

    model_id = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

    messages = [{
        "role": "user",
        "content": [
            {"text": "다음은 요약된 약관 조항 리스트입니다:\n\n" + json.dumps(summarized_list, ensure_ascii=False)}
        ]
    }]

    response = client.converse(
        modelId=model_id,
        system=[{"text": SYSTEM_PROMPT_TOS_EVALUATE}],
        messages=messages,
    )

    print("TOS Evaluation Response:")
    print(response)

    text = response['output']['message']['content'][0]['text']

    # JSON 파싱
    start = text.find('{')
    end = text.rfind('}') + 1
    json_text = text[start:end]

    data = json.loads(json_text)

    # 전체 등급 누락 시 자동 보정
    if not data.get("overall_evaluation"):
        data["overall_evaluation"] = count_score(data["evaluation_for_each_clause"])

    return data

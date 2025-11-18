import json
import boto3

PROMPT_TOS_SUMMARY = """
다음은 한 서비스의 약관 전문입니다. 이 약관에서 소비자가 반드시 알아야 하는 
중요한 조항 10개를 추출하고, 각 조항을 한 문장으로 요약하십시오.

중요한 조항을 판단할 기준은 다음과 같습니다:
1. 개인정보 수집 항목
2. 개인정보 처리 목적
3. 개인정보 보존 기간
4. 개인정보 제3자 제공
5. 자동 수집 기술(쿠키 등) 사용 여부
6. 책임 제한 조항
7. 계약 해지·탈퇴 조건
8. 요금/결제/환불 규정
9. 이용자의 의무·금지사항
10. 약관 변경(일방적 변경 가능성 포함)

규칙:
- 반드시 10개의 JSON 객체를 포함하는 배열로 출력하십시오.
- 각 JSON 객체는 "topic", "summary" 키를 가져야 합니다.
- 각 summary는 반드시 한 문장으로 작성하십시오.
- 불필요한 설명, 서론, 결론, 코드 블록은 절대 포함하지 마십시오.

출력 예시:
[
    {"topic": "개인정보 수집 항목", "summary": "회사는 서비스 이용을 위해 이름과 이메일을 수집합니다."},
    ...
]

아래는 약관 본문입니다:
"""

def tos_summarize(tos_content):
    system_instruction = [{"text": "당신은 약관 분석 전문가입니다. 중요 조항을 명확한 JSON 배열로 요약하십시오."}]
    
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2"
    )

    model_id = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    messages = [{
        "role": "user",
        "content": [{"text": PROMPT_TOS_SUMMARY + tos_content}]
    }]

    response = client.converse(
        modelId=model_id,
        system=system_instruction,
        messages=messages,
    )

    print("TOS Summarization Response:")
    print(response)

    text = response['output']['message']['content'][0]['text']

    # JSON 부분만 추출
    start = text.find('[')
    end = text.rfind(']') + 1
    json_text = text[start:end]

    try:
        data = json.loads(json_text)
    except:
        # 만약 JSON 오류가 있을 경우 최대한 복구
        json_text = json_text.replace('\n', ' ')
        data = json.loads(json_text)

    # 반드시 10개만 유지
    return data[:10]

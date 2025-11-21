from llm_client import LLMClient

def tos_summarize(tos_content: str, client: LLMClient) -> str:
    system_instruction="""
당신은 약관 분석 전문가입니다.
주어진 텍스트에서 주요 약관 내용을 요약합니다.
한국어로 응답합니다.
"""

    response = client.generate_response(system_instruction, tos_content)

    print("TOS Summarization Response:")
    print(response)

    return response

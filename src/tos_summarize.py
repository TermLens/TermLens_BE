import json
from google import genai
from google.genai import types

def tos_summarize(text_html, client):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction="""
            당신은 약관 분석 전문가입니다.
            주어진 html 페이지에서 주요 약관 내용을 요약합니다.
            한국어로 응답합니다.
            """,
        ),
        contents=text_html,
    )

    return response.text

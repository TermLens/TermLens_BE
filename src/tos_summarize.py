import boto3

def tos_summarize(text_html):
    # Create the Bedrock client
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2"
    )

    # Define the model and message
    model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    messages = [
        {
            "role": "user",
            "content": [
                {"text": text_html}
            ]
        }
    ]

    # Make the API call
    response = client.converse(
        modelId=model_id,
        system="""
당신은 약관 분석 전문가입니다.
주어진 html 페이지에서 주요 약관 내용을 요약합니다.
한국어로 응답합니다.
""",
        messages=messages,
    )

    print("TOS Summarization Response:")
    print(response)

    return response['output']['message']['content'][0]['text']

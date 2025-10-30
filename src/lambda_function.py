import json
import os
from google import genai

def lambda_handler(event, context):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
    model="gemini-2.5-flash-lite", contents="hello to me!"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

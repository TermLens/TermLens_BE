# AWS Lambda 환경 및 로컬 환경 모두 Bedrock 사용

# temperature, top_p는 기본값 temperature 0.2, top_p 0.9로 사용
# 환각 억제 목적

from typing import Any, Dict, List
import boto3
from botocore.config import Config

class LLMClient:
    
    # Bedrock 클라이언트 초기화
    def __init__(self, temperature: float = 0.2, top_p: float = 0.9, small_model_id: str = "us.amazon.nova-micro-v1:0", large_model_id: str = "openai.gpt-oss-20b-1:0"):
        
        self.temperature = temperature
        self.top_p = top_p

        # Bedrock 모델 ID를 소형/대형으로 분리해 보관
        self.small_model_id = small_model_id
        self.large_model_id = large_model_id
        
        # Bedrock 클라이언트 생성
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-west-2",
            config=Config(max_pool_connections=50)
        )

    # Bedrock으로부터 응답 생성
    # 기본은 소형 모델, model_size="large" 전달 시 대형 모델 사용
    def generate_response(self, system_instruction: str, message: str, model_size: str = "small", model_id: str = None) -> str:    
        
        selected_model = model_id
        if selected_model is None:
            selected_model = self.large_model_id if model_size == "large" else self.small_model_id

        response = self.client.converse(
            modelId=selected_model,
            inferenceConfig={
                "temperature": self.temperature,
                # "topP": self.top_p
            },
            system=[{"text": system_instruction}],
            messages=[{"role": "user", "content": [{"text": message}]}]
        )

        # 모델에 따라 응답 구조 처리
        if selected_model.startswith("openai"):
             return response['output']['message']['content'][-1]['text']
        else:
             return response['output']['message']['content'][0]['text']
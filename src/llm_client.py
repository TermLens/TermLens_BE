
# 로컬 테스트 환경에서는 gemini 사용
# AWS Lambda 환경에서는 Bedrock의 Claude 사용

# temperature, top_p는 기본값 temperature 0.2, top_p 0.9로 사용
# 환각 억제 목적

import os
from typing import Any, Dict, List
from google import genai
from google.genai import types
import boto3
from botocore.config import Config

class LLMClient:
    
    # 환경에 따라 LLM 모델 선정 및 클라이언트 초기화
    def __init__(self, temperature: float = 0.2, top_p: float = 0.9, small_model_id: str = "us.amazon.nova-micro-v1:0", large_model_id: str = "openai.gpt-oss-120b-1:0"):
        
        self.temperature = temperature
        self.top_p = top_p

        self.provider = os.getenv("LLM_PROVIDER")
        # Bedrock 모델 ID를 소형/대형으로 분리해 보관
        self.small_model_id = small_model_id
        self.large_model_id = large_model_id
        if (self.provider == "GEMINI"):
            # 로컬 테스트 환경 - gemini
            self.client = genai.Client()
        else:
            # AWS Lambda 환경 - Bedrock Claude
            self.client = boto3.client(
                service_name="bedrock-runtime",
                region_name="us-west-2",
                config=Config(max_pool_connections=50)
            )

    # 응답 생성
    # gemini와 bedrock claude 분기 처리
    def generate_response(self, system_instruction: str, message: str, model_size: str = "small", model_id: str = None) -> str:    
        
        if (self.provider == "GEMINI"):
            return self._generate_response_gemini(system_instruction, message)
        else:
            return self._generate_response_bedrock_claude(
                system_instruction,
                message,
                model_size=model_size,
                model_id=model_id,
            )
    
    # gemini로부터 응답 생성
    def _generate_response_gemini(self, system_instruction: str, message: str) -> str:

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                temperature=self.temperature,
                top_p=self.top_p,
                system_instruction=system_instruction
            ),
            contents=message
        )

        return response.text

    # bedrock Claude로부터 응답 생성
    # 기본은 소형 모델, model_size="large" 전달 시 대형 모델 사용
    def _generate_response_bedrock_claude(self, system_instruction: str, message: str, model_size: str = "small", model_id: str = None) -> str:

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

        # response 구조 print (디버깅 용도)
        print(f"Bedrock response structure: {response}")

        return self._extract_bedrock_text(response)

    def _extract_bedrock_text(self, response: Dict[str, Any]) -> str:
        """
        Bedrock 공급자별 응답 구조 차이를 흡수하여 텍스트를 추출한다.
        """
        output = response.get("output") or {}
        message = output.get("message") or {}

        # content는 모델마다 list/str 등 형태가 다를 수 있음
        content: List[Any] = []
        if isinstance(message.get("content"), list):
            content = message["content"]
        elif isinstance(message.get("content"), str):
            content = [message["content"]]
        elif isinstance(output.get("content"), list):
            content = output["content"]

        texts: List[str] = []
        for item in content:
            if isinstance(item, str):
                texts.append(item)
            elif isinstance(item, dict):
                if isinstance(item.get("text"), str):
                    texts.append(item["text"])
                elif isinstance(item.get("content"), str):
                    texts.append(item["content"])
                elif isinstance(item.get("value"), str):
                    texts.append(item["value"])
                elif isinstance(item.get("data"), str):
                    texts.append(item["data"])

        # 일부 모델은 outputText/text/completion 등 다른 필드에 텍스트를 담을 수 있음
        if not texts:
            fallback_keys = ["outputText", "text", "completion"]
            for key in fallback_keys:
                val = output.get(key) or response.get(key)
                if isinstance(val, str):
                    texts.append(val)
                    break

        if not texts:
            raise ValueError(f"LLM 응답에 텍스트 필드를 찾지 못했습니다: {response}")

        return texts[0]

# app/services/llm_client.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMClient:
    @classmethod
    def get_llm(cls, temperature=0.3):
        """
        切换至 DeepSeek 模型
        """
        api_key = os.getenv("DEEPSEEK_API_KEY")
        model_name = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in .env file")

        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            openai_api_base=base_url  # 关键点：将请求转发到 DeepSeek 服务器
        )
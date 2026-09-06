import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek


load_dotenv()


def create_model():

    return ChatDeepSeek(
        model="deepseek-chat",
        api_key=os.getenv(
            "DEEPSEEK_API_KEY"
        ),
        temperature=0,
        timeout=30,
        max_retries=2,
    )
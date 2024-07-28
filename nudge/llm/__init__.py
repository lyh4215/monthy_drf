from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_openai import ChatOpenAI
import os

# OpenAI 객체를 llm으로 설정
llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), model='gpt-3.5-turbo')
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_community.llms import OpenAI
import os

# OpenAI 객체를 llm으로 설정
llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), model='gpt-3.5-turbo')
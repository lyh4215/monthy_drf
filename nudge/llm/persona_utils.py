from dotenv import load_dotenv
load_dotenv(override=True)

from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from models import Post, Persona
from accounts.models import User
import prompts
import os

llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), model='gpt-3.5-turbo')

#find user's persona
def post_to_str(post_list : list) -> str: 
    post_list_str = ""
    for post in post_list:
        post_str = f"{post.created_at} | {post.body} \n"
        post_list_str += post_str
    return post_list_str

def make_persona(author_id : int) -> str:
    author = User.objects.get(id=author_id)
    post_list = Post.objects.filter(author=author).order_by('-created_at')

    #make the list of the user's diary -> str
    post_list_str = post_to_str(post_list)
    print(post_list_str)
    template = prompts.make_persona_template
    prompt = PromptTemplate.from_template(template = template,
                                        partial_variables={'context': post_list_str},)

    chain = prompt | llm
    output = chain.invoke({})
    persona_string: str = output.content
    persona = Persona.objects.create(user = author, persona = persona_string)
    persona.save()

    return persona_string

def modify_persona(post_list : list) -> str:
    post_list_str = post_to_str(post_list)
    return post_list_str
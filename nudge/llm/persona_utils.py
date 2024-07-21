from dotenv import load_dotenv
load_dotenv(override=True)

from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from models import Post, Persona
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from accounts.models import User
from sample_diary import sample_diary
import prompts
import os

from llm import llm

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

#input : new diary
#modify persona
#output : depression rate
def modify_persona(author_id : int) -> float:
    class NewDiary(BaseModel):
        persona: str = Field(description="persona")
        depression_rate: float = Field(description="depression rate")

    template = prompts.modify_persona_template
    parser = PydanticOutputParser(pydantic_object=NewDiary)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate.from_template(
        template = template,
        partial_variables={"format_instructions": format_instructions})
    chain = prompt | llm | parser
    
    #TODO : make this more specific
    user = User.objects.get(id = author_id)
    persona: str = user.persona.persona

    output = chain.invoke({'context': sample_diary[0], 'author_id': author_id, 'persona': persona})

    depression_rate = output.depression_rate
    persona = output.persona
    user.persona.persona = persona
    user.persona.save()

    return depression_rate
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from blog.models import Post
from nudge.models import Persona
from accounts.models import User

from nudge.llm import llm
import nudge.llm.prompts as prompts
from nudge.llm.pandatic_model import PandaticPersona, PandaticNudgeNecessity

def get_nudge_necessity(post : Post) -> bool:
    template = prompts.nudge_necessity_template
    pydantic_object = PandaticNudgeNecessity

    try:
        persona = post.author.persona.persona
    except:
        persona = 'no persona'
    author = post.author
    recent_posts = Post.objects.filter(author=author).order_by('-created_at')[:5]
    recent_posts_str = post_to_str(recent_posts)
    #TODO : make this more specific
    persona: str = persona
    parser = PydanticOutputParser(pydantic_object=pydantic_object)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate.from_template(
        template = template,
        partial_variables={"format_instructions": format_instructions})
    chain = prompt | llm | parser
    output = chain.invoke({'context': post.pages, 'persona': persona, 'recent_posts': recent_posts_str})

    nudge_necessity = output.nudge_necessity
    if nudge_necessity:
        return True
    else:
        return False

#input : new diary
#modify persona
#output : new persona
def modify_persona(post : Post) -> str:
    try:
        persona = post.author.persona
    except:
        make_persona(post.author)
        persona = post.author.persona
    
    author = post.author
    #TODO : make this more specific
    persona: str = persona.persona

    template = prompts.modify_persona_template
    parser = PydanticOutputParser(pydantic_object=PandaticPersona)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate.from_template(
        template = template,
        partial_variables={"format_instructions": format_instructions})
    chain = prompt | llm | parser
    
    output = chain.invoke({'context': post.pages, 'persona': persona})

    persona = output.persona
    author.persona.persona = persona
    author.persona.save()

    return persona

#initial user's persona
def make_persona(author : User) -> str:
    post_list = Post.objects.filter(author=author).order_by('-created_at')

    #make the list of the user's diary -> str
    post_list_str = post_to_str(post_list)
    template = prompts.make_persona_template
    prompt = PromptTemplate.from_template(template = template,
                                        partial_variables={'context': post_list_str},)

    chain = prompt | llm
    output = chain.invoke({})
    persona_string: str = output.content
    persona = Persona.objects.create(author = author, persona = persona_string)
    persona.save()

    return persona_string

def post_to_str(post_list : list) -> str: 
    post_list_str = ""
    for post in post_list:
        post_str = f"Date : {post.date} | Written at : {post.created_at} | Content : {post.pages} \n"
        post_list_str += post_str
    return post_list_str

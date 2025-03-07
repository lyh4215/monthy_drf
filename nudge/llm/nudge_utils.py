from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage

from typing import Annotated, Literal
from typing_extensions import TypedDict

from datetime import datetime
from accounts.models import User

from nudge.llm.pandatic_model import PandaticNudge, PandaticNudgeList
from nudge.llm import prompts
from nudge import models as nudge_models

from nudge.llm import llm, llm_with_tools, tools


class State(TypedDict):
    messages: Annotated[list, add_messages]
    nudges: PandaticNudgeList
    user: User
    current_nudge_index: int
    output_nudges: PandaticNudgeList

#make nudge graph
def make_nudge(user : User):
    workflow = StateGraph(State)
    tool_node = ToolNode(tools)

    #make graph
    workflow.add_node("make_nudge", make_new_nudge)
    workflow.add_node("nudge_reviewer", nudge_reviewer)
    workflow.add_node("tools", tool_node)
    workflow.add_node("nudge_reviewer_end", nudge_reviewer_end)
    
    workflow.add_conditional_edges("nudge_reviewer_end", route_nudge, {"review_more": "nudge_reviewer", "__end__": "__end__"})
    workflow.add_conditional_edges("nudge_reviewer", tools_condition, {"tools": "tools", "__end__": "nudge_reviewer_end"},)
    workflow.add_edge("tools", "nudge_reviewer")
    workflow.add_edge("make_nudge", "nudge_reviewer")

    workflow.set_entry_point("make_nudge")

    nudge_app = workflow.compile()
    #from nudge.llm.print_graph import png
    #png(nudge_app)

    result = nudge_app.invoke({'messages': [], 'user' : user,
                               'current_nudge_index': 0,
                               'output_nudges': PandaticNudgeList(nudges=[])})
    output_nudges : PandaticNudgeList = result['output_nudges']
    for nudge in output_nudges.nudges:
        nudge_models.Nudge.objects.create(author=user,
                                         title=nudge.title,
                                         page=nudge.page,
                                         iconItem=nudge.iconItem,
                                         date = nudge.date,
                                         )
    return output_nudges


#NODES
def make_new_nudge(state):
    template = prompts.make_new_nudge_template
    today = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    user: User= state['user']
    author_id = user.id
    persona = user.persona
    persona_str = persona.persona
    parser = PydanticOutputParser(pydantic_object=PandaticNudgeList)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate.from_template(template=template,
                                        partial_variables={'today': today,
                                                            'persona': persona_str,
                                                            'language': 'korean',
                                                            'format_instructions': format_instructions},)
    
    chain = prompt | llm | parser
    result : PandaticNudgeList = chain.invoke(state)

    return {'messages' : [AIMessage(content = str(result))], 'nudges': result.nudges}

def nudge_reviewer(state):
    nudges: PandaticNudgeList = state['nudges']
    current_nudge_index: int = state['current_nudge_index']
    nudge: PandaticNudge = nudges[current_nudge_index]
    template = prompts.nudge_review_template
    human_message = HumanMessage(content = template.format(nudge=nudge))
    state["messages"] = add_messages(state["messages"], human_message)
    result = llm_with_tools.invoke(state["messages"])

    # We convert the agent output into a format that is suitable to append to the global state
    
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type"}))
    return {
        "messages": [human_message, result],
    }

def nudge_reviewer_end(state):
    current_nudge_index = state['current_nudge_index']
    len_nudges = len(state['nudges'])

    output_nudges : PandaticNudgeList = state['output_nudges']
    output_nudges.append(state['nudges'][current_nudge_index])

    diff = len_nudges - current_nudge_index -1
    if diff == 0:
        return {'messages' : [],
                'current_nudge_index': current_nudge_index +1,
                "output_nudges": output_nudges}
    message = "there is {diff} left. let's review other nudge."
    return {'messages' : [AIMessage(content = message.format(diff = diff))],
            'current_nudge_index': current_nudge_index +1,
            "output_nudges": output_nudges}

def route_nudge(state) -> Literal['nudge_reviewer', '__end__']:
    if state['current_nudge_index'] < len(state['nudges']):
        return "review_more"
    else:
        return '__end__'
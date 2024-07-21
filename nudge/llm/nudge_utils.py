from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage

from typing import Annotated, Literal
from typing_extensions import TypedDict

from datetime import datetime
from accounts.models import User

from pandatic_model import Nudge, NudgeList
import prompts

from llm import llm

#### make nudge
def make_nudge(user_id : int):

    class State(TypedDict):
        messages: Annotated[list, add_messages]
        nudges: NudgeList
        user: User
        current_nudge_index: int
        output_nudges: NudgeList
        

    def make_new_nudge(state):
        template = prompts.make_new_nudge_template
        today = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        user: User= state['user']
        author_id = user.id
        persona = user.persona
        persona_str = persona.persona
        parser = PydanticOutputParser(pydantic_object=NudgeList)
        format_instructions = parser.get_format_instructions()
        prompt = PromptTemplate.from_template(template=template,
                                            partial_variables={'today': today,
                                                               'author_id': author_id,
                                                               'persona': persona_str,
                                                               'language': 'korean',
                                                               'format_instructions': format_instructions},)
        
        chain = prompt | llm | parser
        result : NudgeList = chain.invoke(state)

        return {'messages' : [AIMessage(content = str(result))], 'nudges': result.nudges}

    def nudge_reviewer(state):
        nudges: NudgeList = state['nudges']
        current_nudge_index: int = state['current_nudge_index']
        nudge: Nudge = nudges[current_nudge_index]
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
            "messages": [result],
            "output_nudges": state["output_nudges"].nudges.append(nudge)
        }
    def nudge_reviewer_end(state):
        current_nudge_index = state['current_nudge_index']
        len_nudges = len(state['nudges'])

        output_nudges : NudgeList = state['output_nudges']
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
    workflow = StateGraph(State)

    tool = TavilySearchResults(max_results=2)
    tools = [tool]
    llm_with_tools = llm.bind_tools(tools)
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
    from print_graph import png
    png(workflow)

    user = User.objects.get(id=user_id)
    result = nudge_app.invoke({'messages': [], 'user' : user, 'current_nudge_index': 0})

    print(result['output_nudges'])
    return result['output_nudges']
from langgraph.graph import StateGraph,START,END, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage,AIMessage
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
chekpointer = InMemorySaver()

def llm_call(state):
    message = state['messages']
    response = llm.invoke(message).content
    return {'messages':[AIMessage(content=response)]}
    
graph = StateGraph(MessagesState)
graph.add_node("LLM",llm_call)
graph.add_edge(START,"LLM")
graph.add_edge("LLM",END)

app = graph.compile(checkpointer=chekpointer)

# Backend Test code
# CONFIG = {'configurable': {'thread_id': 'thread-2'}}
# ai_response = app.invoke(
#     {'messages': [HumanMessage(content="I am kanchana")]}, config=CONFIG
# )
# print(ai_response)
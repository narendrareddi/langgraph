from langgraph.graph import StateGraph,START,END, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage,AIMessage
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
DB_PWD = os.getenv('DB_PWD')
DB_URI = f"postgresql://postgres:{DB_PWD}@localhost:5432/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

    def call_model(state: MessagesState):
        response = llm.invoke(state["messages"])
        return {"messages": response}

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_edge(START, "call_model")

    graph = builder.compile(checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "I am 20 y old, what about u?"}]},
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "tell something about me creatievly?"}]},
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
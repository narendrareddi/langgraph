import streamlit as st
from backend import app

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'history' not in st.session_state:
    st.session_state['history']=[]

for msg in st.session_state['history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])
        
user_input = st.chat_input("Type here...")

if user_input:
    with st.chat_message('user'):
        st.text(user_input)
    st.session_state['history'].append({'role':'user','content':user_input})
    
    # # Without Streaming
    # ai_response = app.invoke({'messages':user_input},config=CONFIG)['messages'][-1].content
    # with st.chat_message('assistant'):
    #     st.text(ai_response)
    # st.session_state['history'].append({'role':'assistant','content':ai_response})     
    
    # With Streaming
    with st.chat_message('assistant'):
        ai_response = st.write_stream(
            message.content for message,metadata in app.stream(
                {'messages':user_input},config=CONFIG,stream_mode="messages"
            )
        )
    st.session_state['history'].append({'role':'assistant','content':ai_response})   
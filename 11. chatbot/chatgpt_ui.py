import streamlit as st 
from backend import app
from langchain_core.messages import HumanMessage
import uuid

def generate_thread():
    return uuid.uuid4()

def add_thread(t_id):
    if t_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(t_id)

def chat_reset():
    st.session_state['thread_id'] = generate_thread()
    add_thread(st.session_state['thread_id'])
    st.session_state['history'] = [] 
    
def load_conv(t_id):
    state = app.get_state(config={'configurable': {'thread_id': t_id}})
    return state.values.get('messages', [])


st.sidebar.title('My ChatGPT')

if st.sidebar.button('New Chat'):
    chat_reset()

st.sidebar.header('My Conversations')

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []    

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread()
            
add_thread(st.session_state['thread_id'])       

if 'history' not in st.session_state:
    st.session_state['history'] = []

for t_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(t_id)):
        st.session_state['thread_id']=t_id
        messages = load_conv(t_id)
        temp = []
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp.append({'role':role,'content':msg.content})   
        st.session_state['history'] = temp        

for msg in st.session_state['history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

input_message = st.chat_input('Type here...')

if input_message:
    with st.chat_message('user'):
        st.text(input_message)
    st.session_state['history'].append({'role':'user','content':input_message})
    
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    
    with st.chat_message('assistant'):
        ai_response = st.write_stream(
        msg.content for msg,metadata in app.stream(
            {'messages':input_message},config=CONFIG,stream_mode='messages'
        )
    )
    st.session_state['history'].append({'role':'assistant','content':ai_response})
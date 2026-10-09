import streamlit as st
from agent_graph import run_agent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

st.set_page_config(page_title="LangGraph Agent", page_icon="🤖", layout="wide")
st.title("🤖 LangGraph Research & Math Agent")
st.markdown("This agent can **search the live internet** and **solve complex math**. Watch its thought process!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)
    elif isinstance(msg, ToolMessage):
        with st.expander(f"🛠️ Used Tool: {msg.name}", expanded=False):
            st.code(msg.content, language="text")

if user_query := st.chat_input("Ask me to search the web or solve a math problem..."):
    st.session_state.messages.append(HumanMessage(content=user_query))
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            for step in run_agent(user_query):
                if isinstance(step, ToolMessage):
                    with st.expander(f"🛠️ Using Tool: {step.name}", expanded=True):
                        st.code(step.content, language="text")
                elif isinstance(step, AIMessage):
                    full_response = step.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append(AIMessage(content=full_response))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

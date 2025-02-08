import streamlit as st
import cohere

# response = client.chat(
#     model="command-r-plus", 
#     messages=[{"role": "user", "content": "hello world!"}]
# )
# print(response)

st. title("💬 Disaster Aid Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "message": "I provide real time updates on disasters and measures you can take to keep yourself safe"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["message"])

prompt = st.chat_input()
if prompt:
    # client = cohere. Client (API_KEY)
    client = cohere.ClientV2("n2u2Bg9qC5xmu0G5TrW7IZNS2n1dHlzBFSm8vFIn")
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role":"user","message":prompt})
    response = client.chat( model="command-r-plus-08-2024",messages=st.session_state.messages)
    msg = response.text
    st.session_state.messages.append({"role":"assistant","message":msg})
    st.chat_message("assistant").write(msg)
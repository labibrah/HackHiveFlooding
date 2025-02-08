# import streamlit as st
# import cohere

# # response = client.chat(
# #     model="command-r-plus", 
# #     messages=[{"role": "user", "content": "hello world!"}]
# # )
# # print(response)

# st. title("💬 Disaster Aid Chatbot")

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "message": "I provide real time updates on disasters and measures you can take to keep yourself safe"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["message"])

# prompt = st.chat_input()
# if prompt:
#     # client = cohere. Client (API_KEY)
#     client = cohere.ClientV2("n2u2Bg9qC5xmu0G5TrW7IZNS2n1dHlzBFSm8vFIn")
#     st.chat_message("user").write(prompt)
#     st.session_state.messages.append({"role":"user","content":prompt})
#     response = client.chat( model="command-r-plus-08-2024",messages=st.session_state.messages)
#     msg = response.text
#     st.session_state.messages.append({"role":"assistant","message":msg})
#     st.chat_message("assistant").write(msg)


import streamlit as st
import cohere

st.title("💬 Disaster Aid Chatbot")

# API Key
API_KEY = "n2u2Bg9qC5xmu0G5TrW7IZNS2n1dHlzBFSm8vFIn"
client = cohere.ClientV2(api_key=API_KEY)

# System message for chatbot behavior
system_message = "You provide real-time updates on disasters and safety measures."

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": "Hello! How can I help you stay safe?"}
    ]

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] != "system":  # Don't show system messages in chat
        st.chat_message("user" if msg["role"] == "user" else "assistant").write(msg["content"])

# Get user input
prompt = st.chat_input()
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Streaming response container
    assistant_msg = st.chat_message("assistant")
    response_container = assistant_msg.empty()

    full_response = ""
    
    # Call Cohere API with streaming
    response_stream = client.chat_stream(
        model="command-r-plus-08-2024",
        messages=st.session_state["messages"]
    )

    # Stream the response
    for event in response_stream:
        if event and event.type == "content-delta":
            chunk = event.delta.message.content.text
            full_response += chunk
            response_container.write(full_response)  # Update response dynamically

    # Store the final response in session state
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

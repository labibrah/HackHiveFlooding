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

# Change down below

# import streamlit as st
# import cohere
# import os

# st.title("💬 Disaster Aid Chatbot")

# # API Key
# API_KEY = st.secrets["COHERE_API_KEY"]
# client = cohere.ClientV2(api_key=API_KEY)

# # System message for chatbot behavior
# system_message = "You provide real-time updates on disasters and safety measures."

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [
#         {"role": "system", "content": system_message},
#         {"role": "assistant", "content": "Hello! How can I help you stay safe?"}
#     ]

# # Display chat history
# for msg in st.session_state["messages"]:
#     if msg["role"] != "system":  # Don't show system messages in chat
#         st.chat_message("user" if msg["role"] == "user" else "assistant").write(msg["content"])

# # Get user input
# prompt = st.chat_input()
# if prompt:
#     st.chat_message("user").write(prompt)
#     st.session_state["messages"].append({"role": "user", "content": prompt})

#     # Streaming response container
#     assistant_msg = st.chat_message("assistant")
#     response_container = assistant_msg.empty()

#     full_response = ""
    
#     # Call Cohere API with streaming
#     response_stream = client.chat_stream(
#         model="command-r-plus-08-2024",
#         messages=st.session_state["messages"]
#     )

#     # Stream the response
#     for event in response_stream:
#         if event and event.type == "content-delta":
#             chunk = event.delta.message.content.text
#             full_response += chunk
#             response_container.write(full_response)  # Update response dynamically

#     # Store the final response in session state
#     st.session_state["messages"].append({"role": "assistant", "content": full_response})



import streamlit as st
import cohere
import requests
import time
import threading

st.title("💬 Disaster Aid Chatbot")

# Securely store API key
API_KEY = st.secrets["COHERE_API_KEY"]
client = cohere.Client(API_KEY)

# System message
system_message = "You provide real-time updates on disasters and safety measures."

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": "Hello! How can I help you stay safe?"}
    ]

# Function to fetch weather alerts
def fetch_weather_alerts():
    url = "https://api.weather.gov/alerts/active?area=NY"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        alerts = data.get("features", [])

        if alerts:
            # Extract relevant details from the first alert
            first_alert = alerts[0]["properties"]
            event = first_alert.get("event", "Unknown Event")
            headline = first_alert.get("headline", "No headline available")
            description = first_alert.get("description", "No details available")
            instruction = first_alert.get("instruction", "No safety instructions provided.")

            alert_message = f"🚨 **{event} ALERT** 🚨\n\n📰 {headline}\n\n📌 {description}\n\n🛑 **Safety Instructions:** {instruction}"
        else:
            alert_message = "✅ No active weather alerts. Stay safe! 🌤️ If you need general safety advice, just ask."

        return alert_message
    except Exception as e:
        return f"⚠️ Failed to fetch weather updates: {str(e)}"

# Background thread to fetch alerts every 5 minutes
def weather_alert_thread():
    while True:
        alert_message = fetch_weather_alerts()
        st.session_state["weather_alert"] = alert_message
        time.sleep(300)  # 5-minute interval

# Start background thread once
if "weather_thread_started" not in st.session_state:
    thread = threading.Thread(target=weather_alert_thread, daemon=True)
    thread.start()
    st.session_state["weather_thread_started"] = True

# Display current weather alert
st.subheader("🌍 Live Weather Alert:")
st.write(st.session_state.get("weather_alert", "Fetching latest alerts..."))

# Chat history display
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message("user" if msg["role"] == "user" else "assistant").write(msg["content"])

# User input
prompt = st.chat_input()
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Placeholder for assistant response
    assistant_msg = st.chat_message("assistant")
    response_container = assistant_msg.empty()

    full_response = ""

    # Add weather alert message if relevant
    weather_alert = st.session_state.get("weather_alert", "")
    if "No active weather alerts" not in weather_alert:
        prompt = f"{weather_alert}\n\nUser: {prompt}"

    # Streaming response from Cohere
    response_stream = client.chat_stream(
        model="command-r-plus",
        messages=st.session_state["messages"]
    )

    for event in response_stream:
        if event and hasattr(event, "delta") and event.delta and hasattr(event.delta, "message"):
            chunk = event.delta.message.content
            full_response += chunk
            response_container.write(full_response)  # Update dynamically

    # Save response
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

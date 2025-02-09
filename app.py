import streamlit as st
import cohere
import requests

st.title("💬 Disaster Aid Chatbot")

# Securely store API key
API_KEY = st.secrets["COHERE_API_KEY"]
client = cohere.ClientV2(api_key=API_KEY)  # ✅ Using v2 Client

# State mapping: Full name → Abbreviation
STATE_NAMES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

# Create dropdown with full state names
selected_state = st.selectbox(
    label="📍 Select a state for weather alerts:", 
    options=list(STATE_NAMES.keys()),
    index=31,   # default is NY
)

# Get the abbreviation for the selected state
selected_area = STATE_NAMES[selected_state]

# Initialize session state
if "latest_alert" not in st.session_state:
    st.session_state["latest_alert"] = "🔄 Fetching latest alerts..."

# 🚀 **Function to fetch weather alerts**
def fetch_weather_alerts(area_code):
    url = f"https://api.weather.gov/alerts/active?area={area_code}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        alerts = data.get("features", [])

        if alerts:
            first_alert = alerts[0]["properties"]
            event = first_alert.get("event", "Unknown Event")
            headline = first_alert.get("headline", "No headline available")
            description = first_alert.get("description", "No details available")
            instruction = first_alert.get("instruction", "No safety instructions provided.")

            return f"🚨 **{event} ALERT for {selected_state} ({area_code})** 🚨\n\n📰 {headline}\n\n📌 {description}\n\n🛑 **Safety Instructions:** {instruction}"
        else:
            return f"✅ No active weather alerts in {selected_state} ({area_code}). Stay safe! 🌤️ If you need general safety advice, just ask."

    except Exception as e:
        return f"⚠️ Failed to fetch weather updates: {str(e)}"

# 🚀 **Ensure alert is fetched when the state changes**
if "last_state" not in st.session_state or st.session_state["last_state"] != selected_state:
    new_alert = fetch_weather_alerts(selected_area)
    st.session_state["latest_alert"] = new_alert
    st.session_state["last_state"] = selected_state  # Update state tracking

    # Clear messages when dropdown state changes
    if "messages" in st.session_state:
        st.session_state.pop("messages")

# ✅ **Create system message with updated weather context**
system_message = {
    "role": "system",
    "content": f"You provide real-time updates on disasters and safety measures.\n\nCurrent Alert for {selected_state}:\n{st.session_state['latest_alert']}"
}

# ✅ Initialize chatbot memory only once
if "messages" not in st.session_state:
    st.session_state["messages"] = [system_message]

# ✅ **Display only once in UI**
st.subheader(f"🌍 Live Weather Alert for {selected_state}:")
st.write(st.session_state["latest_alert"])

# ✅ Display chat history (WITHOUT REPEATING THE WEATHER ALERT)
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message("user" if msg["role"] == "user" else "assistant").write(msg["content"])

# User input (Fix: Always visible)
prompt = st.chat_input("Ask me about the weather or safety measures!")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Placeholder for assistant response
    assistant_msg = st.chat_message("assistant")
    response_container = assistant_msg.empty()

    # Construct proper v2 messages format
    messages = [system_message] + st.session_state["messages"]

    # Fetch chat response from Cohere v2
    response = client.chat(
        model="command-r-plus-08-2024",  # ✅ Using v2 model
        messages=messages
    )

    # ✅ Extract correct response content
    full_response = response.message.content[0].text if response.message.content else "Sorry, I couldn't generate a response."

    # Display assistant response
    response_container.write(full_response)

    # Save response
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
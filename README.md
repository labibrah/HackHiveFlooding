# 💬 A.Iert (Disaster Aid Chatbot)

## Overview
A.Iert (pronunced uh-lurt) is an AI-powered chatbot that provides real-time disaster alerts and safety information, specifically designed to help rural communities prepare for natural disasters like floods.

## Features
- 🌍 **Live Weather Alerts** – Fetches real-time disaster updates from the National Weather Service.
- 🤖 **AI Chatbot** – Provides safety recommendations and emergency preparedness tips.
- 📍 **Location-Based Alerts** – Users can select their state to receive relevant warnings.
- ⚡ **Fast & Lightweight** – Built with Streamlit for easy deployment and accessibility.

## How to Run Locally

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/disaster-aid-chatbot.git
cd disaster-aid-chatbot
```

### 2. **Set Up a Virtual Environment (Optional, but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Set Up API Keys**
Create a .streamlit/secrets.toml file and add:
```bash
COHERE_API_KEY="your-cohere-api-key"
```
### 5. **Run the Application**
```bash
streamlit run app.py
```

### 6. **Deployment**
To deploy on Streamlit Cloud, push your changes to GitHub and link the repository to Streamlit Cloud.

Contributing
Feel free to fork this project and submit pull requests with improvements!
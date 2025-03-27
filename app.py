import streamlit as st
from ai_agent import get_groq_response, web_search
import base64

# Set page title and favicon
st.set_page_config(page_title="AI Agent", page_icon="🤖", layout="wide")

# Custom CSS for modern UI
def add_custom_css():
    st.markdown(
        """
        <style>
            body {
                background-color: #0e1117;
                color: white;
            }
            .chat-container {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                max-width: 800px;
                margin: auto;
            }
            .stTextInput input, .stFileUploader div, .stTextArea textarea {
                border-radius: 15px !important;
                padding: 10px;
            }
            .stButton button {
                border-radius: 15px;
                background: linear-gradient(135deg, #1d2671, #c33764);
                color: white;
                font-weight: bold;
            }
            .user-message {
                background: linear-gradient(135deg, #3a3d40, #18191a);
                color: white;
                padding: 10px;
                border-radius: 15px;
                margin: 5px 0;
            }
            .ai-message {
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: white;
                padding: 10px;
                border-radius: 15px;
                margin: 5px 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()

st.markdown("<h1 style='text-align: center;'>🤖 Advanced AI Chatbot</h1>", unsafe_allow_html=True)

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    role = "user-message" if message["role"] == "user" else "ai-message"
    st.markdown(f'<div class="{role}">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# File upload (PDF & Images)
uploaded_file = st.file_uploader("Upload a PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
if uploaded_file:
    file_details = {"File Name": uploaded_file.name, "File Type": uploaded_file.type}
    st.write(file_details)

# User text input (Voice input removed)
user_input = st.text_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
    
    response = get_groq_response(user_input)
    st.session_state.messages.append({"role": "ai", "content": response})
    st.markdown(f'<div class="ai-message">{response}</div>', unsafe_allow_html=True)
    
    search_results = web_search(user_input)
    if search_results:
        st.markdown("<h3>🌐 Related Search Results:</h3>", unsafe_allow_html=True)
        for result in search_results:
            if isinstance(result, dict) and "title" in result and "url" in result:
                st.markdown(f'<a href="{result["url"]}" target="_blank">{result["title"]}</a>', unsafe_allow_html=True)

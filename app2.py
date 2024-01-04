import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize chat model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(
    page_title="Silly",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# Inject custom CSS for dark theme
dark_theme = """
    <style>
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .sidebar .sidebar-content {
            background-color: #000000; /* Set to black */
            color: #FFFFFF;
        }
        .main .block-container {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .streamlit-button {
            color: #1E1E1E;
            background-color: #1E1E1E;
        }
        .streamlit-button:hover {
            color: #FFFFFF;
            background-color: #777777;
        }
    </style>
"""
st.markdown(dark_theme, unsafe_allow_html=True)

# Header and introduction
st.header("👽Silly👽")
st.markdown("**Olá! Estou aqui para ajudar. Pergunte-me qualquer coisa sobre vocês!**")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize input_text and enter_pressed in session state
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'enter_pressed' not in st.session_state:
    st.session_state.enter_pressed = False

# Text area for user input
input_text = st.text_area("Você: ", key="input", height=100, help="Pressione Ctrl & Enter para enviar")

# Check if Enter key is pressed and there is input text
if st.button("Enviar...") or (input_text and st.session_state.enter_pressed):
    st.session_state.enter_pressed = False  # Reset the Enter key flag
    response = get_gemini_response(input_text)

    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("😀 Você:", input_text))
    st.subheader("Resposta:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Silly 🤖:", chunk.text))

# Capture Enter key event
if st.session_state.enter_pressed is False and st.session_state.input_text != input_text:
    st.session_state.enter_pressed = True
    st.session_state.input_text = input_text

# Sidebar with chat history and image
with st.sidebar:
    st.sidebar.image("https://drive.google.com/uc?id=1rlsxYq4l4JAJoun-JcKYNAT1Lasn2lHK", use_column_width=True)
    st.subheader("...Histórico do chat...")

    for role, text in st.session_state['chat_history']:
        st.write(f"{role} {text}")

    st.sidebar.empty()

    with st.sidebar.expander("Mais detalhes"):
        st.write("""
            Apenas uma imagem.
            Escolhi essa imagem porque é *inspiradora* para mim...
        """)
        st.image("https://drive.google.com/uc?id=1QhD1er0my6BNWxqt_RFGpCBXpPesdw19", caption="Minha inspiração, amo essa mulher")

# Note about the chatbot
st.info("Este é um chatbot treinado com dados do **Google**.")

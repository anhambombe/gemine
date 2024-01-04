## loading all the environment variables
from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
import os
import google.generativeai as genai


########################################### configuração da pagina
############################################ Largura da pagina

about_text = """
**Dashboard de dados das campanhas**

Bem-vindo ao nosso aplicativo! 
Estamos empolgados por você estar aqui e gostaríamos de compartilhar algumas informações sobre o que oferecemos e nosso propósito.

**Missão e Objetivo**

Nosso aplicativo foi desenvolvido com o objetivo de fornecer a você uma experiência única e útil. 
Nossa missão é *facilitar o acesso à informação* e *ajudar na tomada de decisões baseadas em dados*. 
Queremos que você aproveite ao máximo nossa plataforma e encontre valor em nossos recursos.

...

"""

menu_items = {
    "About": about_text,
    "Report a bug": "mailto:anhambombe@gmail.com",  # Use o formato correto para um link de e-mail
    "Get help": "https://streamlit.io/community"  # Adicione uma entrada para a página "About" em português
}


# Configure a página
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=menu_items # Use a lista de itens de menu corretamente definida
)
#st.set_page_config(layout="wide")

# Defina a largura desejada em pixels
largura_da_pagina = 1000

# Configure o estilo do layout
st.markdown(f"""
    <style>
        .reportview-container .main .block-container {{
            min-width: {largura_da_pagina}px;
        }}
    </style>
""", unsafe_allow_html=True)
#######################################

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])
def get_gemini_response(question):
    
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app

#st.set_page_config(page_title="Chatbot")

st.header("👽Chatbot👽")
# Introdução
st.markdown("**Olá! Estou aqui para ajudar. Pergunte-me qualquer coisa sobre vocês!**")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Insira a sua pergunta na caixa de texto abaixo👇: ",key="input")
submit=st.button("Enviar...")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("😐", input))
    st.subheader("Resposta:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("🤖", chunk.text))

with st.sidebar:
    st.sidebar.image("https://drive.google.com/uc?id=1rlsxYq4l4JAJoun-JcKYNAT1Lasn2lHK", use_column_width=True)
    #st.sidebar.button("Click me!")
    st.subheader("...Histórico do chat...")
        
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    #st.sidebar.theme = "dark"
    st.sidebar.background_color = "red"
    #st.sidebar.text("This is a text element.")

    #st.sidebar.markdown("Exemplo") #para adicionar texto formatado à sua barra lateral.
    st.sidebar.empty() #para criar um espaço em branco na sua barra lateral.
    #st.sidebar.help("Que tal") #para exibir informações de ajuda sobre a barra lateral.
    #st.sidebar.write("Fim...") #para escrever qualquer objeto Python na barra lateral.

    with st.sidebar.expander("Mais detalhes"):
        st.write("""
            Apenas uma imagem.
            Escolhi essa imagem porque é *inspiradora* para 
            mim...
        """)
        #st.image("https://static.streamlit.io/examples/dice.jpg")
        #st.image("C:\\Users\\LENOVO\\Documents\\DATA_ANALYSIS\\PYTHOH\\PySCRIPS\\2023\\gemineAI\\gemine1\\ai.jpeg")
        st.image("https://drive.google.com/uc?id=1QhD1er0my6BNWxqt_RFGpCBXpPesdw19",caption="Minha inspiração, amo essa mulher")
        #https://drive.google.com/file/d/1QhD1er0my6BNWxqt_RFGpCBXpPesdw19/view?usp=sharing

# Nota sobre o chatbot
st.info("Este é um chatbot treinado com dados do **Google**.")
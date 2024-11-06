import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY
import base64
import os

# Directorio donde se guardarán los archivos
upload_dir = "uploads"

# Crear el directorio si no existe
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, mode=0o755)  # Permisos 755 (rwxr-xr-x)


# Configuración de la API de Gemini
genai.configure(api_key="AIzaSyDOMI3iuGgkiBIxY-prmD9O9Z1ED2A7jOA")

# Configuración del modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # Ajuste de configuraciones de seguridad
    # Ver https://ai.google.dev/gemini-api/docs/safety-settings
)

# Función para iniciar una sesión de chat con el modelo
def start_chat_session():
    return model.start_chat(history=[])

# Función para enviar un mensaje al modelo y obtener una respuesta
def get_response(chat_session, user_input):
    response = chat_session.send_message(user_input)
    return response.text

# Función para codificar la imagen en base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Configuración de la página
st.set_page_config(layout="wide")

# CSS personalizado con gradiente oscuro de fondo, títulos con gradiente rosado claro, y campo de entrada con fondo similar
st.markdown("""
<style>
body {
    color: white;
    background: linear-gradient(to right, #4A0E4E, #170B3B);
}
.stApp {
    background-image: url("data:image/png;base64,%s"), linear-gradient(to right, #4A0E4E, #170B3B);
    background-position: right center, center;
    background-repeat: no-repeat, repeat;
    background-size: contain, cover;
}
.main .block-container {
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    background: linear-gradient(to right, #FFB6C1, #FFC0CB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}
/* Estilo para el campo de entrada */
.stTextInput > div > div > input {
    background: linear-gradient(to right, #4A0E4E, #170B3B);
    color: white;
    border: 1px solid #FFB6C1;
    border-radius: 5px;
}
.stTextInput > div > div > input:focus {
    box-shadow: 0 0 5px #FFB6C1;
}
.stButton > button {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
}
.stMarkdown {
    color: white;
}
</style>
""" % get_base64_of_bin_file('Estef-AI.jpeg'), unsafe_allow_html=True)

# Crear el contenedor del grid
grid = st.container()

# Usar columnas dentro del grid
with grid:
    col1, col2 = st.columns([2, 3])  # Ajustamos las proporciones de las columnas

    with col1:
        st.title("Estef-AI")
        st.write("Bienvenido a Estef-AI, tu asistente virtual especializada en electrónica. Pregúntame lo que necesites saber sobre electrónica.")

        # Campo de entrada de texto para el usuario
        user_input = st.text_input("Escribe tu pregunta aquí:")

        # Botón para enviar la pregunta
        if st.button("Enviar"):
            if user_input:
                chat_session = start_chat_session()
                response = get_response(chat_session, user_input)
                st.write("Estef-AI dice:")
                st.write(response)
            else:
                st.write("Por favor, escribe una pregunta.")

    # La columna 2 se deja vacía para que la imagen de fondo sea visible
    with col2:
        pass  # No añadimos contenido aquí para dejar espacio a la imagen de fondo

import streamlit as st
import google.generativeai as genai
import requests
from google.generativeai.types import FunctionDeclaration, Tool
from dotenv import load_dotenv
import os

load_dotenv()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Chatbot Clima AI",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌦️ Assistente Meteorológico Inteligente")
st.caption("Powered by Google Gemini & Open-Meteo API")

# --- FUNÇÕES DE FERRAMENTA (BACKEND) ---
# (Mesmas funções do código anterior, otimizadas para cache se necessário)

WEATHER_MAP = {
    0: "Céu limpo ☀️", 1: "Predominantemente claro 🌤️", 2: "Parcialmente nublado ⛅", 3: "Nublado ☁️",
    45: "Nevoeiro 🌫️", 48: "Nevoeiro com geada ❄️", 51: "Garoa leve 🌧️", 53: "Garoa moderada 🌧️",
    61: "Chuva fraca ☔", 63: "Chuva moderada ☔", 65: "Chuva forte ⛈️",
    80: "Pancadas de chuva 🌦️", 95: "Tempestade ⚡", 99: "Tempestade com granizo 🌨️"
}

def get_coordinates(city_name):
    """Busca latitude e longitude de uma cidade."""
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=pt&format=json"
        response = requests.get(url)
        data = response.json()
        if not data.get("results"): return None, None
        location = data["results"][0]
        return location["latitude"], location["longitude"]
    except:
        return None, None

def get_weather_forecast(city_name: str):
    """Obtém a previsão do tempo para os próximos dias."""
    lat, lon = get_coordinates(city_name)
    if lat is None: return f"Erro: Cidade '{city_name}' não encontrada."

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "forecast_days": 4, "timezone": "America/Sao_Paulo"
    }

    try:
        resp = requests.get(url, params=params).json()
        daily = resp.get("daily", {})
        
        report = []
        for i in range(len(daily.get("time", []))):
            code = daily["weathercode"][i]
            cond = WEATHER_MAP.get(code, "Desconhecido")
            report.append(
                f"- Data: {daily['time'][i]} | Condição: {cond} | "
                f"Máx: {daily['temperature_2m_max'][i]}°C | "
                f"Mín: {daily['temperature_2m_min'][i]}°C | "
                f"Chuva: {daily['precipitation_sum'][i]}mm"
            )
        return "\n".join(report)
    except Exception as e:
        return f"Erro na API: {str(e)}"

# --- LÓGICA DO CHATBOT ---
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    # Configura o Gemini apenas se a chave for fornecida
    genai.configure(api_key=api_key)
    
    # Inicializa o Histórico de Chat na Sessão (Memória visual do Streamlit)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Inicializa a Sessão do Gemini (Lógica do Modelo)
    if "chat_session" not in st.session_state:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            tools=[get_weather_forecast],
            system_instruction="""
            Você é um meteorologista simpático. Use a função disponível para ver o clima.
            Formate a resposta usando Markdown para deixá-la bonita (use negrito em temperaturas, emojis, etc).
            Não mostre dados técnicos brutos, faça um resumo agradável.
            """
        )
        st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)

    # 1. Exibir mensagens antigas na tela
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 2. Capturar nova entrada do usuário
    if prompt := st.chat_input("Pergunte sobre o clima (ex: Vai chover em SP amanhã?)"):
        
        # Exibe a mensagem do usuário
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Processamento da IA
        with st.chat_message("assistant"):
            with st.spinner("Consultando satélites e modelos meteorológicos..."):
                try:
                    # Envia para o Gemini
                    response = st.session_state.chat_session.send_message(prompt)
                    
                    # Exibe a resposta
                    st.markdown(response.text)
                    
                    # Salva no histórico
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
else:
    st.warning("👈 Por favor, insira sua API Key na barra lateral para começar.")
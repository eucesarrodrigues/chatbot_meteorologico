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

# Mapeamento de códigos WMO (conforme solicitado no desafio)
WEATHER_MAP = {
    0: "Céu limpo ☀️", 1: "Predominantemente claro 🌤️", 2: "Parcialmente nublado ⛅", 3: "Nublado ☁️",
    45: "Nevoeiro 🌫️", 48: "Nevoeiro com geada ❄️", 51: "Garoa leve 🌧️", 53: "Garoa moderada 🌧️",
    61: "Chuva fraca ☔", 63: "Chuva moderada ☔", 65: "Chuva forte ⛈️",
    80: "Pancadas de chuva 🌦️", 95: "Tempestade ⚡", 99: "Tempestade com granizo 🌨️"
}

def get_coordinates(city_name):
    """Busca latitude e longitude de uma cidade usando Open-Meteo."""
    # ... (Mantenha a função get_coordinates aqui, sem alterações) ...
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=pt&format=json"
        response = requests.get(url)
        data = response.json()
        
        if not data.get("results"):
            return None, None
            
        location = data["results"][0]
        return location["latitude"], location["longitude"]
    except Exception as e:
        return None, None

def get_current_weather(city_name: str):
    """
    Obtém a condição climática ATUAL (tempo real) para uma cidade específica.
    Args:
        city_name: O nome da cidade (ex: Tóquio, São Paulo).
    Returns:
        Uma string com o clima em tempo real.
    """
    print(f"\n[SISTEMA] Consultando clima atual para: {city_name}...")
    
    lat, lon = get_coordinates(city_name)
    
    if lat is None or lon is None:
        return f"Erro: Não foi possível encontrar a localização da cidade '{city_name}'."

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code", # Endpoint de clima ATUAL
        "timezone": "America/Sao_Paulo"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        current_data = data.get("current", {})
        temp = current_data.get("temperature_2m", "N/A")
        code = current_data.get("weather_code")
        condition = WEATHER_MAP.get(code, "Condição desconhecida")
        
        report = (
            f"Clima ATUAL: {condition} | "
            f"Temperatura: {temp}°C"
        )
        return report

    except Exception as e:
        return f"Erro ao conectar com a API de clima atual: {str(e)}"

def get_weather_forecast(city_name: str):
    # ... (Mantenha a função get_weather_forecast original aqui, sem alterações) ...
    print(f"\n[SISTEMA] Consultando previsão de 4 dias para: {city_name}...")
    
    lat, lon = get_coordinates(city_name)
    
    if lat is None or lon is None:
        return f"Erro: Não foi possível encontrar a localização da cidade '{city_name}'."

    # Configuração da API Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "forecast_days": 4, # Escopo do projeto: próximos 4 dias
        "timezone": "America/Sao_Paulo"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        daily = data.get("daily", {})
        times = daily.get("time", [])
        codes = daily.get("weathercode", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])

        forecast_list = []
        for i in range(len(times)):
            condition = WEATHER_MAP.get(codes[i], "Condição desconhecida")
            day_info = (
                f"Data: {times[i]} | "
                f"Condição: {condition} | "
                f"Máx: {max_temps[i]}°C | "
                f"Mín: {min_temps[i]}°C | "
                f"Chuva: {precip[i]}mm"
            )
            forecast_list.append(day_info)

        return "\n".join(forecast_list)

    except Exception as e:
        return f"Erro ao conectar com a API de clima: {str(e)}"
    
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
        tools_list = [get_weather_forecast, get_current_weather]

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash', # Versão atualizada!
            tools=tools_list,
            system_instruction="""
            Você é um assistente meteorológico útil e preciso. Você tem acesso a duas ferramentas:
            1. 'get_current_weather': Use esta ferramenta SE O USUÁRIO PERGUNTAR explicitamente sobre o clima 'ATUAL', 'AGORA' ou 'EM TEMPO REAL'.
            2. 'get_weather_forecast': Use esta ferramenta SE O USUÁRIO PERGUNTAR sobre a 'PREVISÃO', 'AMANHÃ', ou para os 'PRÓXIMOS DIAS'.
            
            Diretrizes:
            - Sempre que o usuário perguntar sobre o tempo, escolha e use a ferramenta correta.
            - Se o usuário perguntar sobre o passado (ex: "Choveu ontem?"), explique educadamente que sua base de dados cobre apenas o clima atual e a previsão futura de 4 dias.
            - Formate a resposta de forma limpa, simpática e profissional usando Markdown.
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
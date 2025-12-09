## 📝 Código Markdown Atualizado (`README.md`)

Este arquivo inclui as seguintes modificações:

1.  Inclusão do **`python-dotenv`** nas dependências e na seção de instalação.
2.  Atualização da versão do modelo para **Gemini 2.5 Flash**.
3.  Atualização da seção **"Configuração da API Key"** para refletir o uso do arquivo `.env`.

<!-- end list -->


# 🌦️ Chatbot Meteorológico Inteligente

Este projeto consiste no desenvolvimento de um chatbot que utiliza **Inteligência Artificial Generativa (GenAI)** para interpretar perguntas em linguagem natural sobre o clima e fornecer a previsão do tempo dos próximos 4 dias, utilizando dados em tempo real. A aplicação é construída em Python usando **Streamlit** para a interface web e o modelo **Gemini 2.5 Flash** com a funcionalidade de *Function Calling*.

---

## ⚙️ Arquitetura do Projeto

O chatbot opera em um fluxo robusto e modular, orquestrado pela capacidade de **Function Calling (Chamada de Função)** do modelo Gemini:

1.  **Interface (Streamlit):** Recebe a entrada do usuário através de um chat e exibe a resposta final, mantendo o histórico da conversa (`st.session_state`).
2.  **Orquestração (Gemini 2.5 Flash):**
    * **Interpretação:** O modelo analisa a pergunta e a intenção do usuário (ex: "Qual o clima em SP?").
    * **Chamada de Função:** O modelo decide chamar a função Python `get_weather_forecast`, extraindo o nome da cidade.
3.  **Fonte de Dados (Open-Meteo API):** O código Python executa a função, consulta a API (Geocoding + Forecast) e retorna os dados de previsão (temperatura, precipitação, condição) ao modelo.
4.  **Geração de Resposta:** O Gemini recebe os dados brutos e gera a resposta final em linguagem natural, formatada em Markdown, para o usuário.

---

## 📦 Requisitos e Instalação

### Pré-requisitos

* Python 3.8+
* Chave de API do Google Gemini (obtida via [Google AI Studio](https://aistudio.google.com/api-keys))

### 1. Estrutura de Arquivos

```

.
├── app.py              \# Código principal do Chatbot (Streamlit + Gemini)
├── .env                \# Arquivo para salvar a chave da API (PRÁTICA DE SEGURANÇA)
└── requirements.txt    \# Dependências do projeto

````

### 2. Instalação de Dependências

Crie ou atualize o arquivo `requirements.txt` com o seguinte conteúdo:

```txt
google-generativeai
streamlit
requests
python-dotenv  # Adicionado para carregar a chave da API
````

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

-----

## 🔑 Configuração da API Key (Usando python-dotenv)

Para manter sua chave de API segura e fora do código-fonte, utilize o arquivo `.env`:

1.  Obtenha sua chave no [Google AI Studio](https://aistudio.google.com/api-keys).
2.  Crie um arquivo chamado **`.env`** na raiz do projeto.
3.  Adicione a sua chave no arquivo no formato:

<!-- end list -->

```
# Conteúdo do arquivo .env
GEMINI_API_KEY="SUA_CHAVE_AQUI" 
```

O arquivo `app.py` deve ser modificado para carregar essa chave automaticamente (substituindo o input na barra lateral).

-----

## ▶️ Execução da Aplicação

Inicie a aplicação web através do Streamlit com o seguinte comando:

```bash
streamlit run app.py
```

O aplicativo será aberto automaticamente no seu navegador em `http://localhost:8501`.

-----

## 💬 Exemplos de Interação

O chatbot é projetado para ser **resiliente** a variações de linguagem, tratando tanto perguntas diretas quanto contextuais:

| Entrada do Usuário | Intenção Principal | Resposta Esperada |
| :--- | :--- | :--- |
| **"Vai chover em São Paulo amanhã?"** | Foco em Chuva/Amanhã | Resposta concisa sobre a precipitação do dia seguinte |
| **"Qual a previsão completa para Campinas?"** | Foco no horizonte de 4 dias | Resumo formatado da previsão dos próximos 4 dias |
| **"Qual o clima atual de Tóquio?"** | Foco no dia atual/condição | Informação sobre a condição e temperatura para o dia de hoje |
| **"Choveu ontem em Belo Horizonte?"** | Foco no Passado | Explicação educada sobre a limitação de escopo (apenas 4 dias futuros) |

-----

## 💡 Decisões Técnicas Chave

  * **Gemini 2.5 Flash:** Utilização da versão mais recente do modelo para obter melhor desempenho em latência e raciocínio.
  * **python-dotenv:** Implementado para gerenciar variáveis de ambiente, garantindo que a chave de API seja carregada de forma segura e não exposta no código.
  * **Function Calling (Tool Use):** Utilização da capacidade do Gemini de invocar a função `get_weather_forecast` automaticamente. Isso torna o código Python mais limpo e a lógica de interpretação de linguagem mais robusta.
  * **Gestão de Estado (`st.session_state`):** Essencial no Streamlit para armazenar a sessão do Gemini e o histórico visual do chat, garantindo a continuidade da conversa.
  * **Open-Meteo API:** Escolhida por ser *free tier*, não exigir chave de API e fornecer endpoints de Geocoding (busca por cidade) e Forecast, ideal para o escopo de 4 dias do projeto.

<!-- end list -->

```
```

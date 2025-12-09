# Chatbot Meteorológico — Versão Final

Este projeto implementa um chatbot meteorológico capaz de interpretar perguntas em linguagem natural e retornar previsões do tempo usando GenAI + APIs meteorológicas (CPTEC/INPE via BrasilAPI e fallback WeatherAPI).

## Estrutura do Projeto
```
chatbot_meteo/
│── main.py
│── README.md
│── requirements.txt
│── tests/
│   └── test_previsao.py
└── examples/
    └── fluxo_interacao.md
```

## Execução
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

A rota disponível:
```
GET /clima?pergunta=Vai chover amanhã em Fortaleza?
```

## Pontos de Destaque
- Extração de intenção e cidade via LLM
- Normalização robusta de texto (remoção de acentos)
- Fallback de APIs: CPTEC → WeatherAPI
- Resposta humanizada por modelo generativo
- Testes automatizados com pytest

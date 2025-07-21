# Tarefa 2: Configurar Arquivos Base e Ambiente

## Objetivo
Criar todos os arquivos de configuração base necessários para o projeto.

## Passos

- [ ] [1.2.1] Criar `.env.example` com variáveis do Google Cloud (Speech-to-Text, Vision, TTS)
- [ ] [1.2.2] Criar `requirements.txt` com dependências exatas do ADK
- [ ] [1.2.3] Criar `.gitignore` apropriado
- [ ] [1.2.4] Criar `README.md` inicial
- [ ] [1.2.5] Criar `CLAUDE.md` com instruções do projeto
- [ ] [1.2.6] Criar `pyproject.toml` com configurações Python

## Conteúdo dos Arquivos

### .env.example
- GOOGLE_CLOUD_PROJECT_ID
- GOOGLE_CLOUD_SPEECH_TO_TEXT_KEY
- GOOGLE_CLOUD_VISION_KEY
- GOOGLE_CLOUD_TEXT_TO_SPEECH_KEY
- GEMINI_API_KEY
- ENV (development/production)

### requirements.txt
- google-adk
- fastapi
- uvicorn
- pydantic
- google-cloud-speech
- google-cloud-vision
- google-cloud-texttospeech
- python-multipart
- python-dotenv

### .gitignore
- .env
- __pycache__/
- *.pyc
- .pytest_cache/
- .coverage
- htmlcov/
- dist/
- build/
- *.egg-info/
Plano de Implementação - Professor Virtual ADK (Revisado)

    FASE 1: PREPARAÇÃO E ESTRUTURA BASE

    1. Criar Estrutura de Diretórios do Projeto

    - Criar estrutura dentro de /professor_adk/ (já existente)
    - Criar professor_virtual/ como pacote principal
    - Criar subdiretórios: tools/, providers/, models/, utils/
    - Criar api/ com subdivisões: routes/, middleware/
    - Criar tests/ com subdivisões: unit/, integration/, fixtures/
    - Criar deployment/ e docs/
    - Criar scripts/ para utilitários
    - Adicionar todos os __init__.py necessários

    2. Configurar Arquivos Base e Ambiente

    - Criar .env.example com variáveis do Google Cloud (Speech-to-Text, Vision, TTS)
    - Criar requirements.txt com dependências exatas do ADK
    - Criar .gitignore apropriado
    - Criar README.md inicial
    - Criar CLAUDE.md com instruções do projeto
    - Criar pyproject.toml com configurações Python

    FASE 2: MIGRAÇÃO DOS COMPONENTES OFICIAIS

    3. Migrar e Organizar as Ferramentas (Tools)

    - Extrair transcrever_audio e gerar_audio_tts → tools/audio_tools.py
    - Extrair analisar_necessidade_visual e analisar_imagem_educacional → tools/vision_tools.py
    - Extrair função auxiliar extrair_contexto_educacional → tools/utils.py
    - Criar registro de tools conforme PROFESSOR_TOOLS do implementation.py
    - Manter assinaturas e retornos exatamente como especificado

    4. Migrar Modelos de Dados

    - Converter AnaliseVisualResult dataclass → Pydantic model em models/vision.py
    - Converter AnaliseImagemResult dataclass → Pydantic model em models/vision.py
    - Criar modelos adicionais para request/response em models/api.py
    - Criar modelos de sessão em models/session.py

    5. Migrar Instruction Providers

    - Copiar todos os providers do instruction_providers.py → providers/instructions.py
    - Manter INSTRUCTION_PROVIDERS dict
    - Manter SIMPLE_TEMPLATES dict
    - Preservar assinaturas com ReadonlyContext

    FASE 3: IMPLEMENTAÇÃO DO CORE ADK

    6. Implementar Configurações Baseadas no architecture.json

    - Criar config.py com todas as configurações do architecture.json
    - Definir configuração do LlmAgent (name, model, tools)
    - Incluir generate_content_config (temperature: 0.7, max_output_tokens: 1000)
    - Adicionar configuracoes_globais (timeouts, limites, formatos suportados)
    - Configurar audios_pre_gravados conforme especificado

    7. Implementar o Agente Principal

    - Criar agent.py com LlmAgent conforme architecture.json
    - Configurar as 4 tools: transcricao_audio_tool, analise_necessidade_visual_tool, analise_imagem_tool, gerar_audio_resposta_tool
    - Usar professor_instruction_provider como instruction
    - Implementar InMemoryRunner conforme especificado
    - Configurar InMemorySessionService com suporte a artefatos

    8. Implementar Sistema de Artefatos ADK

    - Configurar gestão de artefatos na sessão usando InMemorySessionService
    - Implementar criação de artefatos para áudio recebido
    - Implementar criação de artefatos para imagem capturada
    - Implementar recuperação de artefatos por nome nas ferramentas
    - Configurar limpeza automática de artefatos antigos

    9. Integrar com APIs do Google Cloud

    - Implementar cliente Google Cloud Speech-to-Text em utils/speech.py
    - Implementar cliente Google Cloud Vision em utils/vision.py 
    - Implementar cliente Google Cloud Text-to-Speech em utils/tts.py
    - Criar wrappers com fallback para modo desenvolvimento

    FASE 4: API E FLUXO DE REQUISIÇÕES

    10. Implementar API REST com FastAPI

    - Criar api/app.py como aplicação principal
    - Implementar api/routes/audio.py para upload e processamento de áudio
    - Implementar api/routes/image.py para captura condicional de imagem
    - Implementar api/routes/chat.py para orquestrar o fluxo completo
    - Adicionar api/routes/health.py para health checks

    11. Implementar o Fluxo Principal Conforme architecture.json

    - Endpoint para receber áudio e criar artefato na sessão
    - Executar transcrição passando nome do artefato (não base64)
    - Analisar necessidade visual com texto transcrito
    - Condicional: solicitar imagem e criar artefato se necessário
    - Processar com agente usando referências aos artefatos
    - Implementar TTS sob demanda retornando nome do artefato
    - Cliente recupera artefato de áudio pelo nome para reprodução

    FASE 5: TRATAMENTO DE ERROS E LOGGING

    12. Implementar Sistema de Logs e Monitoramento

    - Criar utils/logging.py com configuração centralizada
    - Adicionar logs em cada ferramenta
    - Implementar métricas de performance
    - Criar dashboards de monitoramento básico

    13. Implementar Tratamento de Erros

    - Usar providers de erro (erro_instruction_provider)
    - Implementar retry logic para APIs externas
    - Adicionar validações de entrada (formatos, tamanhos)
    - Criar respostas amigáveis para falhas

    FASE 6: TESTES

    14. Criar Testes Unitários

    - Testar cada ferramenta isoladamente
    - Testar providers com diferentes contextos
    - Testar validações e limites
    - Criar mocks para APIs do Google Cloud

    15. Criar Testes de Integração

    - Testar fluxo completo: áudio → resposta
    - Testar fluxo com imagem
    - Testar casos de erro
    - Testar performance e timeouts

    FASE 7: SCRIPTS E DOCUMENTAÇÃO

    16. Criar Scripts de Desenvolvimento

    - scripts/run_dev.py para executar localmente
    - scripts/test_tools.py para testar ferramentas
    - scripts/validate_api.py para validar endpoints

    17. Documentar o Sistema

    - Criar docs/API.md com especificação dos endpoints
    - Criar docs/SETUP.md com instruções de instalação
    - Criar docs/TOOLS.md documentando cada ferramenta
    - Adicionar exemplos de uso

    FASE 8: PREPARAÇÃO PARA PRODUÇÃO

    18. Configurar Docker

    - Criar Dockerfile multi-stage otimizado
    - Criar docker-compose.yml para desenvolvimento
    - Adicionar health checks
    - Configurar volumes para logs

    19. Preparar Deploy Inicial

    - Configurar variáveis de ambiente de produção
    - Adicionar rate limiting básico
    - Configurar CORS apropriado
    - Criar script de deploy simples

    ---
    📋 Observações Importantes:

    1. Manter total alinhamento com implementation.py, architecture.json e instruction_providers.py
    2. Usar LlmAgent único com 4 FunctionTools
    3. Implementar fluxo exato do fluxo_principal em architecture.json
    4. Preservar assinaturas e retornos das ferramentas
    5. TTS apenas sob demanda (botão play)
    6. Foco em robustez desde o início
    7. Usar padrão de Artefatos ADK em vez de base64 para dados binários
    8. Economizar tokens passando apenas referências (nomes) aos artefatos
1. Ferramentas no ADK: Definição, Execução e Contexto
Esta seção aborda a criação e o comportamento das ferramentas (Tools) no Google ADK. Inclui detalhes sobre como instanciar FunctionTool, definir seus metadados, o tratamento de funções síncronas e assíncronas, e a utilização do ToolContext para interação e acesso ao estado.

1.1. Instanciação e Parâmetros do FunctionTool
Como definir name e description para FunctionTool e a relação com BaseTool. No Google ADK, o name e a description de uma FunctionTool não são definidos diretamente no construtor. Em vez disso, o name da ferramenta é inferido do nome da função Python que ela envolve. A description é extraída automaticamente da docstring (ou comentários acima) dessa função. O framework do ADK irá encapsular automaticamente uma função Python como uma FunctionTool quando ela é atribuída à lista de tools de um agente.[1][2]
Discussão sobre decoradores ou métodos alternativos para configuração. A documentação não mostra alternativas para definir name e description de forma explícita no construtor do FunctionTool ou via decoradores @adk_tool para este propósito específico. O método padrão é confiar no nome da função e sua docstring.
Exemplos de código práticos.
        # Sua função Python que será uma ferramenta
        def get_current_weather(location: str, unit: str = "celsius") -> dict:
            """
            Obtém a temperatura atual para um local e unidade especificados.

            Args:
                location: O nome da cidade ou região.
                unit: A unidade de temperatura (e.g., "celsius", "fahrenheit").

            Returns:
                Um dicionário com a temperatura atual e o local.
            """
            # Lógica para obter o clima...
            weather_data = {"location": location, "temperature": 25, "unit": unit}
            return weather_data

        # Instanciação do Agente que usará a ferramenta
        from google.adk.agents import Agent
        from google.genai import types

        # O framework irá automaticamente criar um FunctionTool a partir de get_current_weather
        # O nome da ferramenta será "get_current_weather" e a descrição virá da docstring.
        weather_agent = Agent(
            name="WeatherAgent",
            model="gemini-1.5-flash", # Exemplo de modelo
            description="Um agente que pode obter informações meteorológicas.",
            tools=[get_current_weather] # Passa a função diretamente
        )
        ```
1.2. Execução Assíncrona com FunctionTool e LongRunningFunctionTool
Suporte de FunctionTool para funções async. O FunctionTool do ADK é projetado para encapsular funções síncronas. Se uma função for assíncrona (async def) ou demorar um tempo significativo para ser concluída, a solução apropriada é usar o LongRunningFunctionTool.
O papel de BaseTool.run_async. O BaseTool.run_async é um método que o framework do ADK chama para executar a ferramenta, e não implica que a função encapsulada pelo FunctionTool deva ser assíncrona.[1][3][4]
Uso e propósito de LongRunningFunctionTool. Este gerencia operações que podem ser suspensas e retomadas, permitindo que o agente continue trabalhando em outras tarefas enquanto a operação assíncrona é executada.
Mecanismos de wrapper automático de async para sync. Não há um wrapper automático de async para sync fornecido pelo ADK para FunctionTool. A abordagem recomendada para funções assíncronas é sempre o LongRunningFunctionTool.
        # Função Síncrona com `FunctionTool`
        def calculate_sync_sum(a: int, b: int) -> dict:
            """Calcula a soma de dois números."""
            return {"result": a + b}

        # Função Assíncrona/Longa Duração com `LongRunningFunctionTool`
        import asyncio
        from google.adk.tools import LongRunningFunctionTool

        async def fetch_large_dataset_async(query: str) -> dict:
            """
            Simula uma operação assíncrona de longa duração para buscar um grande conjunto de dados.
            """
            await asyncio.sleep(5) # Simula trabalho assíncrono
            return {"data_summary": f"Dataset for '{query}' fetched successfully after 5 seconds."}

        # Encapsular a função assíncrona com LongRunningFunctionTool
        long_running_tool = LongRunningFunctionTool(func=fetch_large_dataset_async)
        ```
1.3. ToolContext: Parâmetros, Acesso ao Estado e Retornos
A assinatura padrão das funções de ferramenta e a passagem do ToolContext. As funções de ferramenta no ADK podem receber um parâmetro especial tool_context do tipo ToolContext para acessar informações contextuais e o estado da sessão. Este parâmetro pode ser o primeiro ou um dos parâmetros, mas geralmente é colocado como o último.
Como acessar session_state e outros recursos via ToolContext. O ToolContext permite acesso ao session_state através de sua propriedade .state (ex: tool_context.state). O acesso via tool_context.session não é a forma correta para o dicionário de estado, conforme confirmado em issues da comunidade.[8]
Visão geral dos métodos e atributos disponíveis no ToolContext. Além do .state, o ToolContext expõe atributos como .agent_name e .invocation_id.
Formato esperado para o retorno de valores das ferramentas. As ferramentas devem retornar um dicionário Python. Se um tipo diferente de um dicionário for retornado, o framework o encapsulará em um dicionário com a chave "result".[1][4][6][7]
        from google.adk.tools import ToolContext
        from typing import Dict, Any

        def minha_ferramenta_com_contexto(param1: str, param2: int, tool_context: ToolContext) -> Dict[str, Any]:
            """
            Exemplo de ferramenta que usa ToolContext para acessar o estado da sessão.
            """
            session_data = tool_context.state.get("user_data", {})
            agent_name = tool_context.agent_name
            invocation_id = tool_context.invocation_id
            
            # Modificar o estado da sessão
            tool_context.state["tool_last_run"] = "minha_ferramenta_com_contexto"

            return { "status": "success" }
        ```
2. Configuração do Agente e Geração de Conteúdo
Esta seção foca em como os agentes ADK são configurados, especialmente em relação à interação com modelos de linguagem e a personalização de instruções.

2.1. Configuração de Geração de Conteúdo (GenerateContentConfig)
Parâmetros aceitos em types.GenerateContentConfig (temperature, max_tokens, top_p, top_k, stop_sequences). O types.GenerateContentConfig permite configurar como o modelo de linguagem responde. Parâmetros como temperature, max_output_tokens e top_p são válidos e comumente usados. Outros parâmetros confirmados incluem safety_settings e tools.
Localização da documentação completa e especificidades por modelo (Gemini vs. outros). A documentação completa para esses parâmetros pode ser encontrada na documentação mais ampla da API Gemini, da qual o ADK se baseia.[2][9][10][11] A documentação geral do Gemini API (que o ADK utiliza) é a fonte mais completa para detalhes específicos de cada modelo.[9][10][12]
        from google.genai import types

        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=1000,
            top_p=0.95,
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.OFF,
                ),
            ],
        )

        from google.adk.agents import Agent
        my_configured_agent = Agent(
            name="ConfiguredAgent",
            model="gemini-2.0-flash",
            generate_content_config=generate_content_config,
            instruction="Responda de forma concisa e útil."
        )
        ```
2.2. Modelos Gemini Suportados no ADK
Lista e esclarecimento dos modelos Gemini disponíveis (gemini-1.5-flash, gemini-1.5-pro, etc.). O ADK suporta o uso direto de modelos Gemini e também permite o acesso a modelos via Vertex AI Model Garden ou integração com LiteLLM para outros provedores. Modelos como gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash e gemini-2.5-flash são mencionados ou demonstrados em exemplos. O gemini-2.5-flash é confirmado como suportado.
Métodos para verificar modelos disponíveis em runtime. Não há uma API explícita no ADK para listar modelos disponíveis em tempo de execução; a lista completa deve ser consultada na documentação da API Gemini.[2][7][10][11][12]
Diferenças e casos de uso recomendados para cada modelo. As diferenças são inerentes aos próprios modelos Gemini (capacidade de contexto, velocidade, custo, multimodalidade, etc.). O ADK abstrai a interação, mas o desenvolvedor deve escolher o modelo apropriado com base nos requisitos da aplicação.
        from google.adk.agents import Agent

        # Usando gemini-2.5-flash (confirmado como suportado)
        agent_flash_2_5 = Agent(
            name="FlashAgent2_5",
            model="gemini-2.5-flash",
            instruction="Você é um assistente rápido com acesso a ferramentas avançadas de pesquisa."
        )
        ```
2.3. Sistema de Templates e InstructionProvider
Conceito e finalidade de InstructionProvider. Para implementar templates dinâmicos para o campo instruction, o ADK oferece o conceito de InstructionProvider. É uma função Python (ou classe que se comporta como uma função) que você passa para o parâmetro instruction de um agente, em vez de uma string estática. Essa função recebe um objeto ReadonlyContext (ou InvocationContext em alguns casos), permitindo que você acesse o estado da sessão e outras informações contextuais para construir a instrução dinamicamente.
Suporte nativo a motores de template como Jinja2. O ADK não possui suporte nativo explícito a motores de template como Jinja2, mas você pode facilmente integrá-los dentro da sua função InstructionProvider customizada.[13] Para injeções de estado mais simples, sem lógica complexa ou condições, o ADK suporta Using {key} Templating diretamente na string de instrução. No entanto, para lógica condicional ou formatação avançada, o InstructionProvider é a abordagem recomendada.[13]
Como implementar e usar um InstructionProvider customizado para instruções dinâmicas.
        from google.adk.agents import LlmAgent
        from google.adk.agents.readonly_context import ReadonlyContext
        # Opcional: para integrar Jinja2 (precisa instalar: pip install Jinja2)
        # from jinja2 import Template

        # Exemplo de InstructionProvider customizado
        def my_dynamic_instruction_provider(context: ReadonlyContext) -> str:
            """
            Constrói a instrução do agente dinamicamente com base no estado da sessão.
            """
            user_name = context.state.get("user:name", "usuário")
            user_language = context.state.get("user:language", "Português")
            app_mode = context.state.get("app:mode", "normal")

            # Exemplo sem Jinja2:
            instruction_string = (
                f"Você é um assistente útil e amigável. "
                f"Converse com {user_name} em {user_language}. "
                f"O modo atual da aplicação é '{app_mode}'. "
                f"Sempre responda de forma concisa e direta."
            )
            
            # Exemplo com Jinja2 (se integrado):
            # template = Template("Você é um assistente útil e amigável. Converse com {{ user_name }} em {{ user_language }}. O modo atual da aplicação é '{{ app_mode }}'.")
            # instruction_string = template.render(user_name=user_name, user_language=user_language, app_mode=app_mode)
            
            return instruction_string

        # Instanciando um agente com o InstructionProvider
        dynamic_agent = LlmAgent(
            name="DynamicAgent",
            model="gemini-1.5-flash",
            instruction=my_dynamic_instruction_provider # Passa a função aqui
        )

        # O framework irá chamar my_dynamic_instruction_provider(context) antes de cada turno do LLM.

        # Para injeção simples de estado (sem InstructionProvider), use templating {key} na string:
        # story_generator = LlmAgent(
        #     name="StoryGenerator",
        #     model="gemini-2.0-flash",
        #     instruction="""Escreva uma pequena história sobre um gato, focando no tema: {user:favorite_topic}."""
        # )
        # Neste caso, o ADK tenta injetar valores do estado automaticamente.
        ```
3. Gerenciamento de Estado e Estrutura do Projeto
Esta seção detalha a gestão do estado da sessão dentro dos agentes e as melhores práticas para a organização do código-fonte e importações no ADK.

3.1. Gestão de Estado de Sessão (session_state)
Uso correto dos prefixos (APP_PREFIX, USER_PREFIX, TEMP_PREFIX). O session_state no ADK é um dicionário acessível através do objeto context.state em funções de ferramenta e callbacks (onde context é ToolContext ou CallbackContext). Ele serve para manter informações persistentes ou temporárias entre as interações do agente. O uso correto dos prefixos (APP_PREFIX, USER_PREFIX, TEMP_PREFIX) é por convenção para organizar e controlar a persistência dos dados:
user: (corresponde a USER_PREFIX): Dados persistentes do usuário, válidos entre sessões.
app: (corresponde a APP_PREFIX): Dados persistentes da aplicação, acessíveis globalmente ou por múltiplos usuários.
temp: (corresponde a TEMP_PREFIX): Dados temporários, que não são garantidos a persistir após a invocação atual ou o turno.[6][13]
Melhores práticas para estruturar campos customizados e garantir a persistência. Use tipos serializáveis em JSON (strings, números, listas, dicionários). As modificações no estado via context.state[key] = value dentro de callbacks ou ferramentas são automaticamente rastreadas e persistidas pelo framework, dispensando a necessidade de EventActions(state_delta=...) manual para a maioria dos casos.[13][14] Para persistência em produção, use DatabaseSessionService ou VertexAISessionService.
Tratamento de estruturas de estado complexas. Estruturas complexas são suportadas desde que sejam serializáveis em JSON.
        from google.adk.tools import ToolContext
        import uuid

        # Exemplo em uma função de ferramenta
        def track_user_interaction(query: str, tool_context: ToolContext) -> dict:
            """Registra uma interação do usuário e atualiza o contador de sessões."""
            # Acessar e atualizar estado de usuário persistente
            user_interaction_count = tool_context.state.get("user:interaction_count", 0)
            tool_context.state["user:interaction_count"] = user_interaction_count + 1

            # Acessar e atualizar estado de aplicação persistente
            app_total_queries = tool_context.state.get("app:total_queries", 0)
            tool_context.state["app:total_queries"] = app_total_queries + 1

            # Adicionar um estado temporário (não persistente garantido)
            tool_context.state["temp:last_query_timestamp"] = str(uuid.uuid4()) # Exemplo de dado temp

            print(f"User interactions: {tool_context.state['user:interaction_count']}")
            print(f"App total queries: {tool_context.state['app:total_queries']}")
            print(f"Temp timestamp: {tool_context.state['temp:last_query_timestamp']}") # Pode não persistir

            # Estrutura de dados complexa (se serializável)
            if "user:history" not in tool_context.state:
                tool_context.state["user:history"] = []
            tool_context.state["user:history"].append({"query": query, "timestamp": str(uuid.uuid4())})

            return {"status": "state_updated", "query_processed": query}
        ```
3.2. Estrutura de Módulos e Padrões de Importação
Convenções de nomenclatura de módulos (singular vs. plural, e.g., agents vs. agent). A estrutura de módulos do ADK usa uma combinação de nomes no singular e no plural para pacotes e classes. A convenção geral para importação de classes de alto nível ou agrupamentos lógicos parece ser:
google.adk.agents para classes de agente como LlmAgent, Agent.
google.adk.tools para classes de ferramenta como FunctionTool, ToolContext.
google.adk.sessions para serviços de sessão como InMemorySessionService.
google.adk.runners para o Runner.
google.adk.evaluation para utilitários de avaliação.
Como importar classes, funções e tipos auxiliares corretamente. Tipos auxiliares ou classes de contexto aninhadas são importados de seus submódulos específicos, como google.adk.agents.readonly_context.ReadonlyContext ou google.adk.agents.callback_context.CallbackContext.
Impacto de __all__ nas importações de módulos do ADK. Embora não haja menção explícita de __all__ nas buscas, os exemplos de importação na documentação são consistentes com o padrão Python de importação direta de classes ou funções.[2][6][13][14][15]
        # Importações comuns do ADK:
        from google.adk.agents import Agent, LlmAgent  # Classes de agente (pacote 'agents' no plural)
        from google.adk.tools import FunctionTool, ToolContext # Classes de ferramenta (pacote 'tools' no plural)
        from google.adk.sessions import InMemorySessionService # Serviço de sessão (pacote 'sessions' no plural)
        from google.adk.runners import Runner # Runner (pacote 'runners' no plural)
        from google.adk.evaluation import AgentEvaluator # Avaliador (pacote 'evaluation' no plural)

        # Importações de tipos de contexto específicos de submódulos:
        from google.adk.agents.readonly_context import ReadonlyContext
        from google.adk.agents.callback_context import CallbackContext

        # Importações de tipos GenAI (necessários para conteúdo, etc.):
        from google.genai import types

        # Exemplo de uso:
        my_agent = Agent(name="ExampleAgent", model="gemini-1.5-flash")
        tool_context_instance = ToolContext # Tipo para anotação
        session_service = InMemorySessionService()
        ```
4. Avaliação e Extensibilidade do Agente
Esta seção cobre as abordagens para testar agentes ADK e como estender ou observar seu comportamento por meio de callbacks e hooks.

4.1. Framework de Testes do ADK
O papel do AgentEvaluator e alternativas. O principal framework de testes fornecido pelo ADK é o AgentEvaluator, que é usado para avaliar o desempenho dos agentes. Ele pode ser executado via interface web (ADK Web UI) ou via linha de comando (adk eval).
Formato esperado para eval_dataset_file_path_or_dir. O eval_dataset_file_path_or_dir aceita tanto um caminho completo para um arquivo de dataset de avaliação quanto um diretório. Se for um diretório, o AgentEvaluator explorará recursivamente por todos os arquivos com o sufixo .test.json.
Suporte para testes declarativos (YAML/JSON) e integração com pytest ou unittest. Os datasets de avaliação são definidos em formato JSON. O ADK suporta integração com pytest, permitindo que os testes sejam estruturados como casos de teste pytest assíncronos que chamam o AgentEvaluator.evaluate().[15][16]
        # Supondo que você tenha um arquivo de agente 'my_agent_module.py'
        # e um dataset de avaliação 'my_tests/basic_qa.test.json'

        # Conteúdo de my_tests/basic_qa.test.json (Exemplo de formato JSON para dataset de avaliação):
        # [
        #   {
        #     "description": "Teste de saudação básica",
        #     "query": "Olá, como você está?",
        #     "expected_response": "Olá! Estou bem, obrigado por perguntar. Como posso ajudar você hoje?"
        #   },
        #   {
        #     "description": "Teste de ferramenta de clima",
        #     "query": "Qual a temperatura em São Paulo?",
        #     "expected_tool_use": {
        #       "tool_name": "get_current_weather",
        #       "args": {"location": "São Paulo"}
        #     },
        #     "expected_response_contains": "São Paulo"
        #   }
        # ]

        from google.adk.evaluation.agent_evaluator import AgentEvaluator
        import pytest
        import asyncio
        from pathlib import Path

        # Suponha que seu agente está definido em um módulo acessível
        # Ex: agent_module_path = "path.to.your.agent_module"
        # O módulo deve conter uma variável 'root_agent' que é a instância do seu agente.
        # Para este exemplo, usaremos um placeholder:
        agent_module_path = "app.agent_main" # Caminho para o módulo do seu agente

        @pytest.mark.asyncio
        async def test_my_agent_basic_evaluation():
            """
            Exemplo de teste usando AgentEvaluator com um arquivo .test.json.
            """
            # Caminho para o arquivo ou diretório do dataset de avaliação
            # Crie um diretório 'eval_datasets' e coloque 'my_first_eval.test.json' dentro
            eval_dataset_dir = Path(__file__).parent / "eval_datasets" 

            # Certifique-se de que 'eval_datasets' existe e contém os arquivos .test.json
            # Se você tiver um único arquivo, pode ser:
            # eval_dataset_file = Path(__file__).parent / "my_single_eval.test.json"

            print(f"Executing evaluation for agent module: {agent_module_path}")
            print(f"Using evaluation dataset from: {eval_dataset_dir}")

            try:
                await AgentEvaluator.evaluate(
                    agent_module=agent_module_path,
                    eval_dataset_file_path_or_dir=str(eval_dataset_dir),
                    num_runs=1, # Número de vezes que cada entrada do dataset será avaliada
                    # agent_name="MyRootAgent", # Opcional: nome do agente se não for 'root_agent' padrão
                    # initial_session_file="path/to/initial_session.json" # Opcional: estado inicial da sessão
                )
                print("Agent evaluation completed successfully.")
            except Exception as e:
                pytest.fail(f"Agent evaluation failed: {e}")

        # Para executar este teste, salve como 'test_agent.py' e execute 'pytest' no terminal.
        # Certifique-se de ter os arquivos .test.json no local correto.
        ```
4.2. Callbacks e Hooks no ADK
Assinaturas e parâmetros de before_agent_callback e after_agent_callback. O ADK fornece um sistema robusto de callbacks (também chamados de hooks) que permitem aos desenvolvedores intervir em pontos-chave do ciclo de execução do agente. Existem callbacks de nível de agente, modelo e ferramenta, cada um com escopo e objetos de contexto específicos. As assinaturas dos callbacks variam, mas geralmente recebem um objeto de contexto (CallbackContext ou ToolContext) e podem opcionalmente retornar um valor para modificar o comportamento padrão do framework.[3][15][18][19]
before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]: Executado antes da lógica principal do agente. Se retornar um Content object, o ADK pula a execução do agente e usa esse Content como resposta.[15][18]
after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]: Executado após a lógica principal do agente. Se retornar um Content object, ele substitui a resposta final do agente.[15][18]
before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmRequest]: Executado antes de uma chamada ao LLM. Permite modificar a requisição do LLM.
after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]: Executado após uma chamada ao LLM. Permite inspecionar ou modificar a resposta do LLM.
before_tool_callback(tool_context: ToolContext, tool_name: str, tool_args: Dict[str, Any]) -> Optional[Dict[str, Any]]: Executado antes da execução de uma ferramenta. Pode validar/modificar argumentos ou até mesmo pular a execução da ferramenta retornando um dicionário (que será usado como resultado da ferramenta).
after_tool_callback(tool_context: ToolContext, tool_name: str, tool_result: Dict[str, Any]) -> Optional[Dict[str, Any]]: Executado após a conclusão de uma ferramenta. Permite transformar ou cachear o resultado da ferramenta.
Diferenças entre callbacks de agente, modelo e ferramenta.
Agente-nível: (before_agent_callback, after_agent_callback) Afetam o fluxo de execução completo do agente. Útil para controle de acesso, logging de ciclo de vida, ou curto-circuito de respostas.[3][18][19]
Modelo-nível: (before_model_callback, after_model_callback) Interagem diretamente com as requisições e respostas do LLM. Útil para sanitização de entrada, enriquecimento de resposta, filtragem de conteúdo.[3][18][19]
Ferramenta-nível: (before_tool_callback, after_tool_callback) Ocorrem antes e depois da execução de ferramentas. Útil para validação de argumentos, caching de API, ou transformação de resultados da ferramenta.[3][18][19]
Exemplos práticos de uso para modificar e monitorar o fluxo de execução.
        from google.adk.agents import Agent, LlmAgent
        from google.adk.agents.callback_context import CallbackContext
        from google.adk.tools import ToolContext
        from google.genai import types
        import time

        # 1. Callback de Agente: Logging e Curto-circuito
        def my_before_agent_callback(callback_context: CallbackContext) -> types.Content | None:
            print(f"BEFORE AGENT: Agente '{callback_context.agent.name}' iniciando. Invocation ID: {callback_context.invocation_id}")
            # Exemplo de curto-circuito: se o usuário pedir ajuda e estiver no estado 'bloqueado'
            if callback_context.state.get("user:status") == "blocked":
                return types.Content(parts=[types.Part(text="Desculpe, sua conta está bloqueada.")])
            return None

        def my_after_agent_callback(callback_context: CallbackContext) -> types.Content | None:
            print(f"AFTER AGENT: Agente '{callback_context.agent.name}' finalizado. Total de passos: {callback_context.metrics.get('agent_steps', 0)}")
            final_response = callback_context.content.text if callback_context.content else ""
            return types.Content(parts=[types.Part(text=f"{final_response} (Resposta processada por callback)")])

        # 2. Callback de Modelo: Sanitização e Enriquecimento
        def my_before_model_callback(callback_context: CallbackContext, llm_request: types.GenerateContentRequest) -> types.GenerateContentRequest:
            # Simula sanitização: remover números de cartão de crédito (Exemplo Simplificado)
            for part in llm_request.contents[0].parts:
                if part.text:
                    part.text = part.text.replace("1234-5678-9012-3456", "[REDACTED_CARD]")
            print(f"BEFORE MODEL: Requisição LLM modificada para sanitização.")
            return llm_request

        def my_after_model_callback(callback_context: CallbackContext, llm_response: types.GenerateContentResponse) -> types.GenerateContentResponse:
            # Simula enriquecimento: Adicionar um rodapé à resposta
            if llm_response.candidates and llm_response.candidates[0].content.parts:
                current_text = llm_response.candidates[0].content.parts[0].text
                llm_response.candidates[0].content.parts[0].text = f"{current_text}\n\n[Powered by ADK callbacks]"
            print(f"AFTER MODEL: Resposta LLM enriquecida.")
            return llm_response

        # 3. Callback de Ferramenta: Validação e Caching
        def my_tool_function(param: str) -> dict:
            """Uma ferramenta simples."""
            return {"original_param": param, "processed": param.upper()}

        def my_before_tool_callback(tool_context: ToolContext, tool_name: str, tool_args: dict) -> dict | None:
            print(f"BEFORE TOOL: Chamada para ferramenta '{tool_name}' com argumentos: {tool_args}")
            # Exemplo: validar um parâmetro
            if "param" in tool_args and not tool_args["param"].isalnum():
                return {"error": "Parâmetro inválido para ferramenta."} # Curto-circuita a ferramenta
            
            # Exemplo de caching (pseudo-código)
            # cache_key = f"{tool_name}-{tool_args}"
            # if cache.get(cache_key):
            #     print("BEFORE TOOL: Usando resultado do cache.")
            #     return cache.get(cache_key)
            return None

        def my_after_tool_callback(tool_context: ToolContext, tool_name: str, tool_result: dict) -> dict:
            print(f"AFTER TOOL: Ferramenta '{tool_name}' retornou: {tool_result}")
            # Exemplo: transformar o resultado
            if "processed" in tool_result:
                tool_result["final_output"] = f"Tool processed '{tool_result['processed']}' successfully!"
            
            # Exemplo de caching (pseudo-código)
            # cache_key = f"{tool_name}-{tool_result['original_param']}" # Assumindo param é a chave
            # cache.set(cache_key, tool_result)
            return tool_result

        # Definindo um agente com callbacks
        test_agent = LlmAgent(
            name="CallbackTestAgent",
            model="gemini-1.5-flash",
            instruction="Responda sempre de forma útil e utilize a ferramenta se for relevante.",
            tools=[my_tool_function],
            before_agent_callback=my_before_agent_callback,
            after_agent_callback=my_after_agent_callback,
            before_model_callback=my_before_model_callback,
            after_model_callback=my_after_model_callback,
            before_tool_callback=my_before_tool_callback, # Associa o callback à ferramenta (ou ao agente para todas as ferramentas)
            after_tool_callback=my_after_tool_callback,   # Associa o callback à ferramenta
        )

        # Para usar callbacks em ferramentas específicas, eles são geralmente passados no construtor da ferramenta
        # ou gerenciados pelo agente que os contém. No exemplo acima, os callbacks de ferramenta são associados
        # ao agente, o que significa que eles serão aplicados a todas as ferramentas que o agente usa.
        # A documentação mostra que antes_tool_callback e depois_tool_callback são campos de LlmAgent,
        # o que implica que eles são aplicados a todas as ferramentas usadas por esse agente.
        ```
Fontes:
[src-1] Function tools - Agent Development Kit
[src-2] Develop an Agent Development Kit agent | Generative AI on Vertex AI
[src-3] Deep Dive: Internals of Google's ADK Runtime Architecture (Developer Guide) - Medium
[src-4] Tools - Agent Development Kit
[src-5] How Google's Agent Kit makes adding function tools EASY! - YouTube
[src-6] Context - Agent Development Kit
[src-7] The Complete Guide to Google's Agent Development Kit (ADK) - Sid Bharath
[src-8] ToolContext object has no attribute session · Issue #14 · google/adk-python - GitHub
[src-9] Generating content | Gemini API | Google AI for Developers
[src-10] Model Context Protocol(MCP) with Google Gemini 2.5 Pro — A Deep Dive (Full Code)
[src-11] Grounding with Google Search | Gemini API | Google AI for Developers
[src-12] Generate content with the Gemini API in Vertex AI - Google Cloud
[src-13] State - Agent Development Kit
[src-14] How to use Sessions & State in Google ADK - Google Agent Development Kit for Beginners (Part 5) - YouTube
[src-15] Submodules - Agent Development Kit documentation
[src-16] Why Evaluate Agents - Agent Development Kit
[src-17] ResponseEvaluator._get_score returns NaN and breaks threshold checks · Issue #1281 · google/adk-python - GitHub
[src-18] How to use callbacks in Google ADK ? Google Agent Development Kit for Beginners (Part 7)
[src-19] Google Agent Development Kit: An Elegant Tool Redefining AI Agent Architecture - Medium
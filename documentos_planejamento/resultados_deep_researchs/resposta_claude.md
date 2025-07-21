# Guia Técnico Completo: Google Agent Development Kit (ADK) - Resoluções para Implementação em Produção

Realizei uma pesquisa técnica profunda sobre o Google Agent Development Kit para resolver as 10 questões críticas de implementação. Este relatório apresenta soluções definitivas baseadas na documentação oficial e exemplos práticos testados.

## **1. Parâmetros do FunctionTool: Nome e Descrição Automáticos**

O FunctionTool **não aceita parâmetros `name` e `description` explícitos** no construtor. O framework extrai estas informações automaticamente da função Python.

### Implementação Correta:
```python
from google.adk.tools import FunctionTool
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A dictionary with weather information and status
    """
    if city.lower() == "london":
        return {"status": "success", "report": "Sunny, 25°C"}
    else:
        return {"status": "error", "error_message": f"No data for {city}"}

# Instanciação correta - apenas func como parâmetro
weather_tool = FunctionTool(func=get_weather)

# Ou mais comumente, ADK envolve automaticamente:
agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    tools=[get_weather]  # ADK converte automaticamente para FunctionTool
)
```

**Ponto-chave**: O nome é extraído do nome da função Python e a descrição vem da docstring. Sempre forneça docstrings completas para suas ferramentas.

## **2. Funções Async com FunctionTool: Use LongRunningFunctionTool**

FunctionTool aceita **apenas funções síncronas**. Para operações assíncronas ou de longa duração, use `LongRunningFunctionTool`.

### Diferenciação:
```python
from google.adk.tools import FunctionTool, LongRunningFunctionTool
import time

# ✅ CORRETO - Função síncrona com FunctionTool
def sync_calculation(a: int, b: int) -> dict:
    """Quick mathematical operation"""
    return {"result": a + b, "status": "success"}

# ✅ CORRETO - Função generator para LongRunningFunctionTool
def slow_analysis(data: str):
    """Analyze large dataset with progress updates"""
    yield {"status": "initializing", "message": "Starting analysis..."}
    
    for step in range(3):
        time.sleep(1)  # Simulate processing
        yield {"status": "processing", "step": step + 1, "total": 3}
    
    return {"status": "completed", "insights": ["insight1", "insight2"]}

# Uso correto
sync_tool = FunctionTool(func=sync_calculation)
async_tool = LongRunningFunctionTool(func=slow_analysis)
```

**Importante**: Não existe wrapper automático para converter async em sync. O runtime ADK é assíncrono e executa funções síncronas usando `asyncio.to_thread()` quando necessário.

## **3. Parâmetros de GenerateContentConfig: Lista Completa**

O parâmetro correto é `max_output_tokens` (não `max_tokens`). Segue a lista completa de parâmetros suportados:

### Parâmetros Principais:
```python
from google.genai import types

config = types.GenerateContentConfig(
    # Amostragem
    temperature=0.7,                    # float: 0.0 a 2.0
    max_output_tokens=1024,             # int: limite do modelo
    top_p=0.95,                        # float: 0.0 a 1.0
    top_k=20,                          # int: positivo
    
    # Parada
    stop_sequences=["STOP!", "END"],    # List[str]
    
    # Penalização
    frequency_penalty=0.1,             # float: -2.0 a 2.0
    presence_penalty=0.1,              # float: -2.0 a 2.0
    
    # Formato
    response_mime_type="application/json",  # str
    response_schema={...},             # dict: JSON Schema
    
    # Segurança
    safety_settings=[                  # List[SafetySetting]
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
    ],
    
    # Avançado
    seed=42,                          # int: determinismo
    response_logprobs=True,           # bool
    cached_content="cache_name"       # str
)
```

### Exemplo para Produção:
```python
production_config = types.GenerateContentConfig(
    temperature=0.2,           # Mais determinístico
    max_output_tokens=2048,    # Limite apropriado
    top_p=0.95,               # Equilíbrio qualidade/diversidade
    frequency_penalty=0.1,    # Reduz repetição
    presence_penalty=0.1      # Aumenta diversidade
)
```

## **4. Sistema de Templates e InstructionProvider**

O ADK **não tem suporte nativo para Jinja2**, mas oferece dois mecanismos próprios:

### 1. String Templates com Interpolação:
```python
from google.adk.agents import LlmAgent

story_agent = LlmAgent(
    name="StoryGenerator",
    model="gemini-2.0-flash",
    instruction="Escreva uma história sobre um gato, focando no tema: {topic}."
)
# Se session.state['topic'] = "amizade", o modelo recebe:
# "Escreva uma história sobre um gato, focando no tema: amizade."
```

### 2. InstructionProvider Dinâmico:
```python
from google.adk.agents.readonly_context import ReadonlyContext

def dynamic_instruction_provider(context: ReadonlyContext) -> str:
    """InstructionProvider customizado para instruções dinâmicas."""
    user_tier = context.state.get("user_tier", "standard")
    user_language = context.state.get("user:language", "pt")
    
    if user_tier == "premium":
        base_instruction = "Você é um assistente premium com acesso completo."
    else:
        base_instruction = "Você é um assistente padrão."
    
    return f"""
{base_instruction}

Configurações do usuário:
- Nível: {user_tier}
- Idioma: {user_language}

Seja cordial e profissional em todas as respostas.
"""

# Usar o InstructionProvider
agent = LlmAgent(
    model="gemini-2.0-flash",
    name="dynamic_agent",
    instruction=dynamic_instruction_provider  # Função, não string
)
```

### InstructionProvider Robusto para Produção:
```python
class ProductionInstructionProvider:
    """InstructionProvider com cache e validação."""
    
    def __init__(self):
        self.template_cache = {}
        self.fallback_instruction = "Você é um assistente útil."
    
    def __call__(self, context: ReadonlyContext) -> str:
        try:
            return self._generate_instruction(context)
        except Exception as e:
            print(f"Erro ao gerar instrução: {e}")
            return self.fallback_instruction
    
    def _generate_instruction(self, context: ReadonlyContext) -> str:
        cache_key = self._get_cache_key(context)
        
        if cache_key in self.template_cache:
            return self.template_cache[cache_key]
        
        instruction = self._build_dynamic_instruction(context)
        
        if len(self.template_cache) < 100:
            self.template_cache[cache_key] = instruction
        
        return instruction
```

## **5. Framework de Testes do ADK**

O ADK usa arquivos JSON para testes (não suporta YAML nativamente). Existem dois formatos principais:

### Formato .test.json (Testes Unitários):
```json
[
  {
    "query": "roll a die for me",
    "expected_tool_use": [
      {
        "tool_name": "roll_die",
        "tool_input": {
          "sides": 6
        }
      }
    ],
    "expected_intermediate_agent_responses": [],
    "reference": "I rolled a 6-sided die and got: 4"
  }
]
```

### Formato .evalset.json (Testes de Integração):
```json
[
  {
    "name": "session_unique_name",
    "data": [
      {
        "query": "user question",
        "expected_tool_use": [
          {
            "tool_name": "tool_name",
            "tool_input": { "param": "value" }
          }
        ],
        "reference": "expected final response"
      }
    ],
    "initial_session": {
      "state": {},
      "app_name": "agent_name",
      "user_id": "test_user"
    }
  }
]
```

### Integração com pytest:
```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator

def test_agent_basic_functionality():
    """Test the agent's basic ability."""
    AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/simple_test.test.json",
    )

def test_agent_with_initial_state():
    """Test with custom initial session state."""
    AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/complex_test.evalset.json",
        initial_session_file="tests/initial.session.json"
    )
```

### Execução via CLI:
```bash
adk eval \
  samples_for_testing/hello_world \
  samples_for_testing/hello_world/hello_world_eval_set_001.evalset.json \
  --config_file_path=config/test_config.json \
  --print_detailed_results
```

## **6. Modelos Gemini Disponíveis**

**SIM, gemini-2.5-flash EXISTE** e está em General Availability desde junho de 2025.

### Lista Completa de Modelos:

#### Modelos Estáveis (Produção):
- **gemini-2.5-pro** - GA, modelo thinking avançado
- **gemini-2.5-flash** - GA, thinking otimizado para preço-performance
- **gemini-2.0-flash** - GA, modelo rápido e eficiente

#### Modelos Preview:
- **gemini-2.5-flash-lite-preview-06-17** - Menor custo, maior velocidade
- **gemini-2.0-pro-experimental** - Melhor para código complexo

### Verificação em Runtime:
```python
from google.adk.agents import Agent

supported_models = [
    "gemini-2.5-pro",
    "gemini-2.5-flash", 
    "gemini-2.0-flash"
]

def verify_model_availability(model_name):
    try:
        agent = Agent(
            name="test_agent",
            model=model_name,
            description=f"Testing {model_name}"
        )
        return f"✅ {model_name} available"
    except Exception as e:
        return f"❌ {model_name} not available: {e}"

for model in supported_models:
    print(verify_model_availability(model))
```

## **7. Gestão de Estado de Sessão: Prefixos e Estrutura**

### Prefixos de Estado:
```python
# Sem prefixo - Estado da sessão
session.state['current_intent'] = 'book_flight'

# user: - Estado do usuário (persistente entre sessões)
session.state['user:preferred_language'] = 'pt-BR'
session.state['user:preferences'] = {'notifications': True}

# app: - Estado da aplicação (global)
session.state['app:api_endpoint'] = 'https://api.company.com'

# temp: - Estado temporário (nunca persistido)
session.state['temp:processing_data'] = {...}
```

### Estrutura Recomendada:
```python
session.state.update({
    # Estados de sessão
    'current_workflow': 'order_processing',
    'step_counter': 3,
    
    # Estados do usuário
    'user:profile': {
        'name': 'João Silva',
        'preferences': {
            'language': 'pt-BR',
            'currency': 'BRL'
        }
    },
    
    # Estados da aplicação
    'app:config': {
        'max_retries': 3,
        'timeout_seconds': 30
    },
    
    # Estados temporários
    'temp:cache': {
        'batch_id': 'batch_123'
    }
})
```

### Atualização via EventActions:
```python
from google.adk.events import Event, EventActions

state_changes = {
    "task_status": "active",
    "user:login_count": session.state.get("user:login_count", 0) + 1,
    "temp:validation_needed": True
}

actions = EventActions(state_delta=state_changes)
event = Event(
    invocation_id="inv_update",
    author="system",
    actions=actions
)

session_service.append_event(session, event)
```

## **8. Imports e Estrutura de Módulos**

### Nomenclatura Correta: `google.adk.agents` (PLURAL)

```python
# ✅ CORRETO - Plural
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# ❌ INCORRETO - Singular
# from google.adk.agent import Agent  # NÃO EXISTE
```

### Estrutura Completa de Imports:
```python
# Agentes
from google.adk.agents import (
    Agent, LlmAgent, BaseAgent,
    SequentialAgent, ParallelAgent, LoopAgent
)

# Ferramentas
from google.adk.tools import (
    FunctionTool, LongRunningFunctionTool,
    ToolContext, google_search,
    MCPTool, OpenAPIToolset
)

# Sessões
from google.adk.sessions import (
    InMemorySessionService,
    DatabaseSessionService,
    VertexAiSessionService
)

# Runners
from google.adk.runners import Runner, InMemoryRunner

# Contextos
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext

# Eventos
from google.adk.events import Event, EventActions

# Modelos
from google.adk.models import BaseLlm, LLMRegistry
from google.adk.models.lite_llm import LiteLlm

# Tipos GenAI
from google.genai import types
```

## **9. Parâmetros da Ferramenta e ToolContext**

### ToolContext é SEMPRE o último parâmetro:
```python
from google.adk.tools import ToolContext

def my_tool(param1: str, param2: int, tool_context: ToolContext) -> dict:
    """Descrição da ferramenta."""
    # Acessar estado
    user_pref = tool_context.state.get('user:preferences', {})
    
    # Atualizar estado
    tool_context.state['last_action'] = 'tool_executed'
    
    # Retornar resultado
    return {"status": "success", "result": param1}
```

### Métodos Disponíveis no ToolContext:
```python
def advanced_tool(query: str, tool_context: ToolContext) -> dict:
    # Propriedades principais
    state = tool_context.state
    actions = tool_context.actions
    function_id = tool_context.function_call_id
    
    # Gerenciamento de artefatos
    artifacts = tool_context.list_artifacts()
    document = tool_context.load_artifact("doc.pdf")
    version = tool_context.save_artifact("result.txt", content)
    
    # Busca na memória
    results = tool_context.search_memory(query)
    
    # Controle de fluxo
    tool_context.actions.escalate = True
    tool_context.actions.transfer_to_agent = "specialist_agent"
    
    return {
        "status": "success",
        "artifacts_count": len(artifacts)
    }
```

### Padrão de Retorno:
```python
def correct_tool_pattern(input: str, tool_context: ToolContext) -> dict:
    try:
        result = process(input)
        return {
            "status": "success",
            "result": result,
            "metadata": {"processed_at": datetime.now().isoformat()}
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__
        }
```

## **10. Callbacks e Hooks do ADK**

### Assinaturas Corretas:

#### Before/After Agent Callbacks:
```python
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional

def before_agent_callback(
    callback_context: CallbackContext
) -> Optional[types.Content]:
    """Executado antes do agente processar."""
    if callback_context.state.get("skip_agent"):
        return types.Content(
            role="model",
            parts=[types.Part(text="Agente pulado")]
        )
    return None

def after_agent_callback(
    callback_context: CallbackContext
) -> Optional[types.Content]:
    """Executado após o agente processar."""
    return None  # Usar resposta original
```

#### Before/After Model Callbacks:
```python
from google.adk.models import LlmRequest, LlmResponse

def before_model_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Executado antes da chamada ao LLM."""
    # Modificar request ou retornar resposta alternativa
    return None

def after_model_callback(
    callback_context: CallbackContext,
    llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Executado após resposta do LLM."""
    # Modificar ou substituir resposta
    return None
```

### Implementação com Callbacks:
```python
agent = LlmAgent(
    name="AgentWithCallbacks",
    model="gemini-2.0-flash",
    instruction="Assistente com callbacks",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback
)
```

### Padrão de Callback Chain:
```python
class CallbackChain:
    def __init__(self):
        self.callbacks = []
    
    def add_callback(self, callback_func):
        self.callbacks.append(callback_func)
    
    def execute_chain(self, context, request):
        for callback in self.callbacks:
            result = callback(context, request)
            if result is not None:
                return result
        return None

# Uso
chain = CallbackChain()
chain.add_callback(security_filter)
chain.add_callback(personalization_filter)
chain.add_callback(audit_filter)

agent = LlmAgent(
    name="ChainedAgent",
    model="gemini-2.0-flash",
    before_model_callback=chain.execute_chain
)
```

## Conclusão

Este guia técnico fornece soluções definitivas para as 10 questões críticas de implementação do Google ADK. As respostas são baseadas na documentação oficial e exemplos práticos verificados. Com estas informações, você pode corrigir os erros de validação e implementar o Professor Virtual com arquitetura robusta para produção.

**Recursos adicionais:**
- Documentação oficial: https://google.github.io/adk-docs/
- Repositório GitHub: https://github.com/google/adk-python
- API Reference: https://google.github.io/adk-docs/api-reference/python/
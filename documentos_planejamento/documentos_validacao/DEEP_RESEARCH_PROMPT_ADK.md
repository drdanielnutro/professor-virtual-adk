# Deep Research Prompt - Esclarecimento de Inconsistências ADK

## Contexto
Este documento contém questões específicas sobre o Google Agent Development Kit (ADK) para esclarecer inconsistências encontradas durante validação de implementação. Cada questão precisa de resposta definitiva baseada na documentação oficial ou exemplos práticos do ADK.

## Questões Críticas para Pesquisa

### 1. PARÂMETROS DO FUNCTIONTOOL

**Questão Principal**: Como exatamente o FunctionTool deve ser instanciado quando precisamos definir name e description?

**Pontos Específicos**:
- A documentação mostra apenas `func` como parâmetro do construtor, mas BaseTool tem campos `name` e `description`
- Como definir esses atributos na prática?
- Existe algum decorador ou método alternativo?
- Exemplos oficiais mostram algum padrão?

**O que precisamos descobrir**:
```python
# Opção A - Só func é aceito?
tool = FunctionTool(func=minha_funcao)

# Opção B - Existe alguma forma de passar name/description?
tool = FunctionTool(func=minha_funcao, name="nome", description="desc")

# Opção C - Usa-se outro padrão?
@adk_tool(name="nome", description="desc")
def minha_funcao():
    pass
```

### 2. FUNÇÕES ASYNC COM FUNCTIONTOOL

**Questão Principal**: FunctionTool aceita funções async ou apenas síncronas?

**Pontos Específicos**:
- A documentação diz `Callable`, mas BaseTool tem `run_async`
- Como reconciliar essa aparente contradição?
- LongRunningFunctionTool é a solução para async?
- Existe wrapper automático de async para sync?

**O que precisamos descobrir**:
```python
# Isso funciona?
async def minha_funcao_async():
    await alguma_operacao()
    
tool = FunctionTool(func=minha_funcao_async)

# Ou precisa ser assim?
def minha_funcao_sync():
    return asyncio.run(alguma_operacao())
    
tool = FunctionTool(func=minha_funcao_sync)
```

### 3. PARÂMETROS DE GENERATE_CONTENT_CONFIG

**Questão Principal**: Quais parâmetros são aceitos em `types.GenerateContentConfig`?

**Pontos Específicos**:
- `temperature` e `max_tokens` são válidos?
- Onde está a documentação completa de `types.GenerateContentConfig`?
- Quais outros parâmetros existem?
- É específico do modelo (Gemini vs outros)?

**O que precisamos descobrir**:
```python
generate_content_config = {
    "temperature": 0.7,      # Válido?
    "max_tokens": 1000,      # Válido?
    "top_p": 0.95,          # Existe?
    "top_k": 40,            # Existe?
    "stop_sequences": []     # Existe?
}
```

### 4. SISTEMA DE TEMPLATES E INSTRUCTIONPROVIDER

**Questão Principal**: Como implementar templates dinâmicos para o campo `instruction`?

**Pontos Específicos**:
- O que é exatamente um `InstructionProvider`?
- ADK tem suporte nativo para Jinja2?
- Como criar um InstructionProvider customizado?
- Exemplos de uso com templates?

**O que precisamos descobrir**:
```python
# Como implementar isso corretamente?
class JinjaInstructionProvider(InstructionProvider):
    def __init__(self, template_path):
        self.template = load_jinja_template(template_path)
    
    def get_instruction(self, context):
        return self.template.render(**context)

# Ou existe algo pronto?
instruction = adk.templates.JinjaProvider("template.j2")
```

### 5. FRAMEWORK DE TESTES DO ADK

**Questão Principal**: Como estruturar testes para agentes ADK?

**Pontos Específicos**:
- AgentEvaluator é a única opção?
- Formato esperado do `eval_dataset_file_path_or_dir`?
- Suporte para testes declarativos (YAML/JSON)?
- Integração com pytest ou unittest?

**O que precisamos descobrir**:
```python
# Qual é o formato correto?
AgentEvaluator.evaluate(
    agent_module="app.agent",
    eval_dataset_file_path_or_dir="???"  # Que formato?
)

# Existe algo como?
@adk.test
def test_meu_agente():
    response = agent.run("pergunta")
    assert "esperado" in response
```

### 6. MODELOS GEMINI DISPONÍVEIS

**Questão Principal**: Quais modelos Gemini estão disponíveis no ADK?

**Pontos Específicos**:
- `gemini-2.5-flash` existe ou é `gemini-1.5-flash`?
- Lista completa de modelos suportados?
- Como verificar modelos disponíveis em runtime?
- Diferenças entre modelos para ADK?

**O que precisamos descobrir**:
```python
# Existe algo como?
from google.adk.models import list_available_models
print(list_available_models())

# Ou como validar?
model = "gemini-2.5-flash"  # Válido ou não?
```

### 7. GESTÃO DE ESTADO DE SESSÃO

**Questão Principal**: Como trabalhar corretamente com session_state customizado?

**Pontos Específicos**:
- Uso correto dos prefixos (APP_PREFIX, USER_PREFIX, TEMP_PREFIX)?
- Como estruturar campos customizados?
- Persistência entre requisições?
- Melhores práticas para estado complexo?

**O que precisamos descobrir**:
```python
# Qual é o padrão correto?
state["user_name"] = "João"  # Assim?
state["user:name"] = "João"  # Ou assim?
state["app:user_name"] = "João"  # Ou assim?

# Como estruturar dados complexos?
state["app:historico_duvidas"] = [...]  # Array é suportado?
```

### 8. IMPORTS E ESTRUTURA DE MÓDULOS

**Questão Principal**: Qual é a estrutura correta de imports do ADK?

**Pontos Específicos**:
- É `google.adk.agents` (plural) ou `google.adk.agent` (singular)?
- Todos os módulos seguem o padrão plural?
- Como importar tipos auxiliares?
- Existe __all__ definido nos módulos?

**O que precisamos descobrir**:
```python
# Qual é correto?
from google.adk.agents import LlmAgent
from google.adk.agent import LlmAgent

# E para tools?
from google.adk.tools import FunctionTool, ToolContext
from google.adk.tool import FunctionTool, ToolContext
```

### 9. PARÂMETROS DA FERRAMENTA E TOOLCONTEXT

**Questão Principal**: Como as ferramentas devem receber e usar o ToolContext?

**Pontos Específicos**:
- ToolContext é sempre o último parâmetro?
- Como acessar session_state através do ToolContext?
- Métodos disponíveis no ToolContext?
- Como retornar valores corretamente?

**O que precisamos descobrir**:
```python
# Qual assinatura é correta?
def minha_ferramenta(param1: str, param2: int, tool_context: ToolContext):
    # Como acessar session?
    session = tool_context.session  # Existe?
    state = tool_context.state      # Ou assim?
    
    # Como retornar?
    return {"resultado": "valor"}   # Dict simples?
    return ToolResult(...)          # Ou classe especial?
```

### 10. CALLBACKS E HOOKS DO ADK

**Questão Principal**: Como implementar callbacks corretamente?

**Pontos Específicos**:
- Assinatura correta de before_agent_callback e after_agent_callback?
- Diferença entre callbacks de agent, model e tool?
- Como modificar comportamento através de callbacks?
- Exemplos práticos de uso?

**O que precisamos descobrir**:
```python
# Qual é a assinatura correta?
def before_agent_callback(context: ???) -> ???:
    pass

def after_model_callback(context: ???, response: ???) -> ???:
    pass
```

## Resultado Esperado

Para cada questão acima, precisamos:
1. **Resposta definitiva** baseada em documentação oficial
2. **Exemplo de código** funcional
3. **Link ou referência** para documentação
4. **Alternativas** se houver múltiplas abordagens válidas

## Prioridade

Questões em ordem de impacto para correção:
1. Parâmetros do FunctionTool (crítico)
2. Funções async (crítico)
3. Sistema de templates (importante)
4. Generate content config (importante)
5. Outras questões (útil mas não bloqueante)

---

**NOTA**: Este documento deve ser usado como base para pesquisar na documentação oficial do ADK, exemplos no GitHub do Google, ou através de experimentação prática com o SDK.
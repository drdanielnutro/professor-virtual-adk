# Tarefa 3: Migrar e Organizar as Ferramentas (Tools)

## Objetivo
Extrair e organizar as ferramentas do arquivo `implementation.py` do planejamento oficial.

## Passos

- [ ] [2.1.1] Extrair `transcrever_audio` e `gerar_audio_tts` → `tools/audio_tools.py`
- [ ] [2.1.2] Extrair `analisar_necessidade_visual` e `analisar_imagem_educacional` → `tools/vision_tools.py`
- [ ] [2.1.3] Extrair funções auxiliares (`validar_audio_metadata`, `extrair_contexto_educacional`) → `tools/utils.py`
- [ ] [2.1.4] Criar registro de tools conforme `PROFESSOR_TOOLS` do implementation.py
- [ ] [2.1.5] Manter assinaturas e retornos exatamente como especificado

## Arquivos de Origem
- `/documentos_planejamento/documentos_oficiais/implementation.py`

## Estrutura das Ferramentas

### audio_tools.py
- `transcrever_audio(audio_data: str, formato: str, tool_context: ToolContext) -> Dict[str, Any]`
- `gerar_audio_tts(texto: str, tool_context: ToolContext, velocidade: float = 1.0, voz: str = "pt-BR-Standard-A") -> Dict[str, Any]`

### vision_tools.py
- `analisar_necessidade_visual(texto: str, tool_context: ToolContext) -> Dict[str, Any]`
- `analisar_imagem_educacional(imagem_data: str, contexto_pergunta: str, tool_context: ToolContext) -> Dict[str, Any]`

### utils.py
- `validar_audio_metadata(metadata: Dict[str, Any]) -> Tuple[bool, Optional[str]]`
- `extrair_contexto_educacional(texto: str) -> Dict[str, Any]`

## Importante
- Preservar EXATAMENTE as assinaturas das funções
- Manter estrutura de retorno (Dict com campos específicos)
- Incluir todos os comentários e docstrings originais
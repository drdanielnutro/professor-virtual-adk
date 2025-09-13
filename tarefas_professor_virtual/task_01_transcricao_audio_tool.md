**Task 1: Implementar a ferramenta transcricao_audio_tool**

**Subtask 1.1: Criar a função `transcrever_audio`**
-   **Ação Detalhada:** "Transcreve um artefato de áudio para texto usando serviços de speech-to-text. Esta ferramenta processa o áudio gravado pela criança, que foi previamente salvo como um artefato na sessão, e o converte em texto para que o agente possa entender a pergunta."
-   **Trecho de Código:**
    ```python
    def transcrever_audio(
        nome_artefato_audio: str,
        tool_context: ToolContext
    ) -> Dict[str, Any]:
        """Transcreve um artefato de áudio para texto usando serviços de speech-to-text.
        
        Esta ferramenta processa o áudio gravado pela criança, que foi previamente
        salvo como um artefato na sessão, e o converte em texto para que o agente
        possa entender a pergunta.
        
        Args:
            nome_artefato_audio: O nome do artefato de áudio a ser processado.
                                 Ex: "pergunta_aluno_123.wav"
            tool_context: Contexto da ferramenta ADK, usado para acessar o artefato.
            
        Returns:
            Dict contendo o texto transcrito e metadados...
        """
        try:
            # 1. Acessar o artefato usando o tool_context
            artifact = tool_context.session.get_artifact(nome_artefato_audio)
            if not artifact:
                return {
                    "erro": f"Artefato de áudio '{nome_artefato_audio}' não encontrado na sessão.",
                    "sucesso": False
                }
            
            audio_bytes = artifact.content
            formato = artifact.name.split('.')[-1] if '.' in artifact.name else "desconhecido"

            # 2. Validações (agora sobre os dados reais do artefato)
            formatos_suportados = ["wav", "mp3", "m4a"]
            if formato not in formatos_suportados:
                return {"erro": f"Formato {formato} não suportado", "sucesso": False}
            
            max_size = 10 * 1024 * 1024  # 10MB
            if len(audio_bytes) > max_size:
                return {"erro": "Arquivo de áudio muito grande (máximo 10MB)", "sucesso": False}
            
            # 3. Lógica de negócio (simulada)
            texto_transcrito = "Este é um texto simulado da transcrição do áudio do artefato."
            duracao_segundos = len(audio_bytes) / (16000 * 2)
            
            return {
                "sucesso": True,
                "texto": texto_transcrito,
                "duracao_segundos": duracao_segundos,
                "formato": formato,
                "tamanho_bytes": len(audio_bytes),
                "idioma_detectado": "pt-BR"
            }
            
        except Exception as e:
            return {"erro": f"Erro ao transcrever áudio: {str(e)}", "sucesso": False}
    ```
-   **Localização:** `implementation.py`
-   **Cuidados e Diretrizes:** "O agente DEVE chamar a ferramenta `transcrever_audio` com o argumento `nome_artefato_audio` sendo o nome exato do arquivo fornecido no prompt. A implementação deve validar os formatos (`wav`, `mp3`, `m4a`) e o tamanho máximo (10MB)."
-   **Referência para Verificação:** "Para contexto completo, consulte o arquivo `implementation.py` e verifique se a implementação corresponde à definição em `architecture.json`."

**Subtask 1.2: Verificação de consistência**
-   **Ação Detalhada:** "Verificar no arquivo `architecture.json` se a grafia dos nomes das classes, módulos e ferramentas usados na sub-tarefa anterior está 100% correta."
-   **Trecho de Código:** N/A
-   **Localização:** N/A
-   **Cuidados e Diretrizes:** "Se for encontrada uma discrepância, ela deve ser corrigida para corresponder exatamente à definição no `architecture.json`. Anote qualquer correção necessária."
-   **Referência para Verificação:** "Fonte da verdade para nomes e grafia: `architecture.json`."
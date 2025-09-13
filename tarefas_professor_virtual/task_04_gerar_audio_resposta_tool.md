**Task 4: Implementar a ferramenta gerar_audio_resposta_tool**

**Subtask 4.1: Criar a função `gerar_audio_tts`**
-   **Ação Detalhada:** "Gera um artefato de áudio TTS a partir de um texto. Converte o texto da resposta educacional em áudio e o salva como um novo artefato na sessão. O nome do artefato gerado é retornado para que o aplicativo cliente possa recuperá-lo e reproduzi-lo."
-   **Trecho de Código:**
    ```python
    def gerar_audio_tts(
        texto: str,
        tool_context: ToolContext,
        velocidade: float = 1.0,
        voz: str = "pt-BR-Standard-A"
    ) -> Dict[str, Any]:
        """Gera um artefato de áudio TTS a partir de um texto.
        
        Converte o texto da resposta educacional em áudio e o salva como um novo
        artefato na sessão. O nome do artefato gerado é retornado para que o
        aplicativo cliente possa recuperá-lo e reproduzi-lo.
        
        Args:
            texto: Texto para converter em áudio.
            tool_context: Contexto da ferramenta ADK.
            velocidade: Velocidade da fala (0.5 a 2.0).
            voz: Identificador da voz a usar.
            
        Returns:
            Dict indicando o sucesso e o nome do artefato de áudio criado.
        """
        try:
            if not texto or len(texto.strip()) == 0:
                return {"erro": "Texto vazio fornecido", "sucesso": False}
            
            audio_bytes_simulados = b"audio_data_simulado_tts_" + texto.encode('utf-8')
            
            nome_artefato = f"resposta_tts_{uuid.uuid4()}.mp3"
            
            tool_context.session.create_artifact(
                name=nome_artefato,
                content=audio_bytes_simulados,
                mime_type="audio/mpeg"
            )
            
            return {
                "sucesso": True,
                "nome_artefato_gerado": nome_artefato,
                "tamanho_caracteres": len(texto)
            }
            
        except Exception as e:
            return {"erro": f"Erro ao gerar áudio TTS: {str(e)}", "sucesso": False}
    ```
-   **Localização:** `implementation.py`
-   **Cuidados e Diretrizes:** "Esta ferramenta (`gerar_audio_tts`) só deve ser chamada se o sistema explicitamente pedir para gerar o áudio da resposta final. Normalmente, o agente apenas fornecerá a resposta em texto."
-   **Referência para Verificação:** "Para contexto completo, consulte o arquivo `implementation.py` e `instruction_providers.py` e verifique se a implementação corresponde à definição em `architecture.json`."

**Subtask 4.2: Verificação de consistência**
-   **Ação Detalhada:** "Verificar no arquivo `architecture.json` se a grafia dos nomes das classes, módulos e ferramentas usados na sub-tarefa anterior está 100% correta."
-   **Trecho de Código:** N/A
-   **Localização:** N/A
-   **Cuidados e Diretrizes:** "Se for encontrada uma discrepância, ela deve ser corrigida para corresponder exatamente à definição no `architecture.json`. Anote qualquer correção necessária."
-   **Referência para Verificação:** "Fonte da verdade para nomes e grafia: `architecture.json`."
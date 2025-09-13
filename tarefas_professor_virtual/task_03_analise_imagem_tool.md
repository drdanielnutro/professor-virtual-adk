**Task 3: Implementar a ferramenta analise_imagem_tool**

**Subtask 3.1: Criar a função `analisar_imagem_educacional`**
-   **Ação Detalhada:** "Extrai informações educacionais relevantes de um artefato de imagem. Esta ferramenta processa a imagem capturada (foto do exercício, página do livro), que foi previamente salva como um artefato, e extrai informações relevantes."
-   **Trecho de Código:**
    ```python
    def analisar_imagem_educacional(
        nome_artefato_imagem: str,
        contexto_pergunta: str,
        tool_context: ToolContext
    ) -> Dict[str, Any]:
        """Extrai informações educacionais relevantes de um artefato de imagem.
        
        Esta ferramenta processa a imagem capturada (foto do exercício, página do livro),
        que foi previamente salva como um artefato, e extrai informações relevantes.
        
        Args:
            nome_artefato_imagem: O nome do artefato de imagem a ser processado.
                                  Ex: "exercicio_matematica_001.png"
            contexto_pergunta: Contexto da pergunta original da criança.
            tool_context: Contexto da ferramenta ADK, usado para acessar o artefato.
            
        Returns:
            Dict com análise educacional da imagem.
        """
        try:
            # 1. Acessar o artefato
            artifact = tool_context.session.get_artifact(nome_artefato_imagem)
            if not artifact:
                return {
                    "erro": f"Artefato de imagem '{nome_artefato_imagem}' não encontrado.",
                    "sucesso": False, "qualidade_adequada": False
                }
            
            imagem_bytes = artifact.content

            # 2. Validações
            max_size = 5 * 1024 * 1024  # 5MB
            if len(imagem_bytes) > max_size:
                return {
                    "erro": "Imagem muito grande (máximo 5MB)",
                    "sucesso": False, "qualidade_adequada": False
                }
            
            # 3. Lógica de negócio (simulada)
            resultado = AnaliseImagemResult(
                tipo_conteudo="exercicio_matematica",
                elementos_detectados=["equação quadrática", "gráfico de parábola"],
                contexto_educacional="Exercício de matemática sobre funções quadráticas",
                qualidade_adequada=True, sugestao_acao=None
            )
            if len(imagem_bytes) < 10000:
                resultado.qualidade_adequada = False
                resultado.sugestao_acao = "Imagem pode estar com baixa resolução"
            
            return {
                "sucesso": True, "tipo_conteudo": resultado.tipo_conteudo,
                "elementos_detectados": resultado.elementos_detectados,
                "contexto_educacional": resultado.contexto_educacional,
                "qualidade_adequada": resultado.qualidade_adequada,
                "sugestao_acao": resultado.sugestao_acao,
                "tamanho_bytes": len(imagem_bytes), "contexto_pergunta": contexto_pergunta
            }
            
        except Exception as e:
            return {
                "erro": f"Erro ao analisar imagem: {str(e)}",
                "sucesso": False, "qualidade_adequada": False
            }
    ```
-   **Localização:** `implementation.py`
-   **Cuidados e Diretrizes:** "O agente DEVE chamar a ferramenta `analisar_imagem_educacional` com os argumentos `nome_artefato_imagem` e `contexto_pergunta`. A implementação deve validar o tamanho máximo da imagem (5MB)."
-   **Referência para Verificação:** "Para contexto completo, consulte o arquivo `implementation.py` e `instruction_providers.py` e verifique se a implementação corresponde à definição em `architecture.json`."

**Subtask 3.2: Verificação de consistência**
-   **Ação Detalhada:** "Verificar no arquivo `architecture.json` se a grafia dos nomes das classes, módulos e ferramentas usados na sub-tarefa anterior está 100% correta."
-   **Trecho de Código:** N/A
-   **Localização:** N/A
-   **Cuidados e Diretrizes:** "Se for encontrada uma discrepância, ela deve ser corrigida para corresponder exatamente à definição no `architecture.json`. Anote qualquer correção necessária."
-   **Referência para Verificação:** "Fonte da verdade para nomes e grafia: `architecture.json`."
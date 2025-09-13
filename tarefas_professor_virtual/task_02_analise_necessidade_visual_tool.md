**Task 2: Implementar a ferramenta analise_necessidade_visual_tool**

**Subtask 2.1: Criar a função `analisar_necessidade_visual`**
-   **Ação Detalhada:** "Detecta se há referências visuais no texto que requerem captura de imagem. Esta ferramenta analisa o texto transcrito procurando por palavras e padrões que indicam que a criança está se referindo a algo visual."
-   **Trecho de Código:**
    ```python
    def analisar_necessidade_visual(
        texto: str,
        tool_context: ToolContext
    ) -> Dict[str, Any]:
        """Detecta se há referências visuais no texto que requerem captura de imagem.
        
        Esta ferramenta analisa o texto transcrito procurando por palavras e padrões
        que indicam que a criança está se referindo a algo visual.
        
        Args:
            texto: Texto transcrito da pergunta da criança.
            tool_context: Contexto da ferramenta ADK.
            
        Returns:
            Dict com análise de necessidade visual.
        """
        padroes_visuais = [
            r'\b(esse|esta|esses|estas|aqui|aí|isso|isto)\b', r'\b(mostr\w+|ve[jr]|olh\w+|observ\w+)\b',
            r'\b(figura|imagem|foto|desenho|gráfico|diagrama|exercício|questão|problema)\b',
            r'\b(tá|está)\s+(escrito|mostrando|aparecendo)', r'o que (é|significa|quer dizer) (isso|isto)',
            r'não (entendi|compreendi) (esse|este|essa|esta)', r'(ajuda|me ajude|help) com (isso|este|esse)',
        ]
        texto_lower = texto.lower()
        referencias_encontradas = []
        pontuacao_visual = 0.0
        for padrao in padroes_visuais:
            matches = re.findall(padrao, texto_lower)
            if matches:
                referencias_encontradas.extend(matches)
                pontuacao_visual += len(matches) * 0.15
        if "exercício" in texto_lower or "questão" in texto_lower: pontuacao_visual += 0.3
        if any(word in texto_lower for word in ["esse aqui", "esta aqui", "isso aqui"]): pontuacao_visual += 0.4
        
        confianca = min(pontuacao_visual, 1.0)
        resultado = AnaliseVisualResult(
            necessita_imagem=confianca >= 0.5,
            confianca=confianca,
            referencias_encontradas=list(set(referencias_encontradas))
        )
        return {
            "necessita_imagem": resultado.necessita_imagem, "confianca": resultado.confianca,
            "referencias_encontradas": resultado.referencias_encontradas,
            "justificativa": f"Detectadas {len(resultado.referencias_encontradas)} referências visuais"
        }
    ```
-   **Localização:** `implementation.py`
-   **Cuidados e Diretrizes:** "Após transcrever o áudio, se o texto contiver palavras como 'isso aqui', 'este exercício', 'olha essa figura', o agente DEVE chamar a ferramenta `analisar_necessidade_visual`. Se a ferramenta retornar `necessita_imagem: true`, a resposta para o sistema deve ser: 'Por favor, peça ao usuário para enviar uma foto do exercício.'"
-   **Referência para Verificação:** "Para contexto completo, consulte o arquivo `implementation.py` e `instruction_providers.py` e verifique se a implementação corresponde à definição em `architecture.json`."

**Subtask 2.2: Verificação de consistência**
-   **Ação Detalhada:** "Verificar no arquivo `architecture.json` se a grafia dos nomes das classes, módulos e ferramentas usados na sub-tarefa anterior está 100% correta."
-   **Trecho de Código:** N/A
-   **Localização:** N/A
-   **Cuidados e Diretrizes:** "Se for encontrada uma discrepância, ela deve ser corrigida para corresponder exatamente à definição no `architecture.json`. Anote qualquer correção necessária."
-   **Referência para Verificação:** "Fonte da verdade para nomes e grafia: `architecture.json`."
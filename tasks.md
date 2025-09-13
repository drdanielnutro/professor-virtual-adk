### Análise do Processo Executado

1.  **Loop de Iteração:** Iniciei o processo lendo o array `componentes` dentro de `architecture.json`. Identifiquei 6 componentes a serem processados: 4 ferramentas (`transcricao_audio_tool`, `analise_necessidade_visual_tool`, `analise_imagem_tool`, `gerar_audio_resposta_tool`) e 2 componentes de infraestrutura (`session_service`, `runner`).
2.  **Extração por Tarefa:** Para cada um desses 6 componentes, criei uma "Task". Dentro de cada tarefa, consultei `implementation.py` para extrair o código-fonte exato e `instruction_providers.py` para extrair as regras de negócio e diretrizes de uso.
3.  **Geração do Documento:** Consolidei todas as 6 tarefas em um único documento, seguindo o template de saída obrigatório.

A seguir, o resultado final.

---

# Plano de Implementação: Agente ProfessorVirtual

**Fontes de Dados:**
- `/Users/institutorecriare/VSCodeProjects/professor_direto/documentos_planejamento/documentos_oficiais/architecture.json`
- `/Users/institutorecriare/VSCodeProjects/professor_direto/documentos_planejamento/documentos_oficiais/implementation.py`
- `/Users/institutorecriare/VSCodeProjects/professor_direto/documentos_planejamento/documentos_oficiais/instruction_providers.py`

**Data de Geração:** 2025-07-22T10:38:00Z

---

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

---

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

---

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

---

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

---

**Task 5: Configurar o componente session_service**

**Subtask 5.1: Configurar o serviço de sessão em memória**
-   **Ação Detalhada:** "Configurar o serviço de gerenciamento de sessões em memória, que é essencial para armazenar os ARTEFATOS (áudio e imagem) durante a interação do usuário."
-   **Trecho de Código:**
    ```
    N/A - Componente de configuração do ADK.
    ```
-   **Localização:** "Configuração do ADK runner/aplicação principal."
-   **Cuidados e Diretrizes:** "A classe a ser usada é `InMemorySessionService`. Esta escolha é adequada para prototipagem e desenvolvimento, pois atende aos requisitos sem adicionar a complexidade de um banco de dados externo."
-   **Referência para Verificação:** "Para contexto completo, consulte a seção do componente `session_service` em `architecture.json`."

**Subtask 5.2: Verificação de consistência**
-   **Ação Detalhada:** "Verificar no arquivo `architecture.json` se o nome da classe `InMemorySessionService` está sendo usado corretamente na configuração do runner."
-   **Trecho de Código:** N/A
-   **Localização:** N/A
-   **Cuidados e Diretrizes:** "A grafia deve ser exata para que o ADK possa instanciar o serviço corretamente."
-   **Referência para Verificação:** "Fonte da verdade para nomes e grafia: `architecture.json`."

---

**Task 6: Configurar o componente runner**

**Subtask 6.1: Configurar o executor do agente**
-   **Ação Detalhada:** "Configurar o runner em memória para executar o agente `professor_virtual` e orquestrar o fluxo de trabalho."
-   **Trecho de Código:**
    ```
    N/A - Componente de configuração do ADK.
    ```
-   **Localização:** "Configuração do ADK runner/aplicação principal."
-   **Cuidados e Diretrizes:** "A classe a ser usada é `InMemoryRunner`. Esta escolha é consistente com o `InMemorySessionService` e adequada para desenvolvimento, processando requisições de forma síncrona."
-   **Referência para Verificação:** "Para contexto completo, consulte a seção do componente `runner` em `architecture.json`."

**Subtask 6.2: Verificação de consistência**
-   **Ação Detalhada:** "Verificar no arquivo `architecture.json` se o nome da classe `InMemoryRunner` e o nome do agente (`professor_virtual`) estão sendo usados corretamente na configuração."
-   **Trecho de Código:** N/A
-   **Localização:** N/A
-   **Cuidados e Diretrizes:** "A grafia deve ser exata para que o ADK possa instanciar e executar o agente correto."
-   **Referência para Verificação:** "Fonte da verdade para nomes e grafia: `architecture.json`."
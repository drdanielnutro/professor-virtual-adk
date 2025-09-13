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
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
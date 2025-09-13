# Plano de Implementação: Agente ProfessorVirtual

**Fontes de Dados:**
- `/Users/institutorecriare/VSCodeProjects/professor_direto/documentos_planejamento/documentos_oficiais/architecture.json`
- `/Users/institutorecriare/VSCodeProjects/professor_direto/documentos_planejamento/documentos_oficiais/implementation.py`
- `/Users/institutorecriare/VSCodeProjects/professor_direto/documentos_planejamento/documentos_oficiais/instruction_providers.py`

**Data de Geração:** 2025-07-22T10:38:00Z

## Análise do Processo Executado

1.  **Loop de Iteração:** Iniciei o processo lendo o array `componentes` dentro de `architecture.json`. Identifiquei 6 componentes a serem processados: 4 ferramentas (`transcricao_audio_tool`, `analise_necessidade_visual_tool`, `analise_imagem_tool`, `gerar_audio_resposta_tool`) e 2 componentes de infraestrutura (`session_service`, `runner`).
2.  **Extração por Tarefa:** Para cada um desses 6 componentes, criei uma "Task". Dentro de cada tarefa, consultei `implementation.py` para extrair o código-fonte exato e `instruction_providers.py` para extrair as regras de negócio e diretrizes de uso.
3.  **Geração do Documento:** Consolidei todas as 6 tarefas em um único documento, seguindo o template de saída obrigatório.

## Índice de Tarefas

### Ferramentas
- [Task 1: Implementar a ferramenta transcricao_audio_tool](./task_01_transcricao_audio_tool.md)
- [Task 2: Implementar a ferramenta analise_necessidade_visual_tool](./task_02_analise_necessidade_visual_tool.md)
- [Task 3: Implementar a ferramenta analise_imagem_tool](./task_03_analise_imagem_tool.md)
- [Task 4: Implementar a ferramenta gerar_audio_resposta_tool](./task_04_gerar_audio_resposta_tool.md)

### Componentes de Infraestrutura
- [Task 5: Configurar o componente session_service](./task_05_session_service.md)
- [Task 6: Configurar o componente runner](./task_06_runner.md)

## Resumo

Este diretório contém o plano de implementação completo do Agente ProfessorVirtual, dividido em tarefas individuais para facilitar a navegação e implementação. Cada arquivo contém as subtarefas detalhadas, incluindo código, diretrizes e referências para verificação.
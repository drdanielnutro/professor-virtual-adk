"""
Testes automatizados para o Professor Virtual ADK
Usa pytest e AgentEvaluator do ADK
"""

import pytest
import asyncio
from pathlib import Path
from google.adk.evaluation import AgentEvaluator


class TestProfessorVirtualAgent:
    """Testes para o agente Professor Virtual."""
    
    # Assumindo que o agente está em app.agent
    AGENT_MODULE = "app.agent"
    
    @pytest.mark.asyncio
    async def test_basic_questions(self):
        """Testa perguntas básicas sem necessidade de imagem."""
        test_file = Path(__file__).parent / "unit" / "basic_questions.test.json"
        
        await AgentEvaluator.evaluate(
            agent_module=self.AGENT_MODULE,
            eval_dataset_file_path_or_dir=str(test_file),
            num_runs=1,
            agent_name="professor_virtual"
        )
    
    @pytest.mark.asyncio
    async def test_visual_detection(self):
        """Testa detecção de necessidade visual."""
        test_file = Path(__file__).parent / "unit" / "visual_detection.test.json"
        
        await AgentEvaluator.evaluate(
            agent_module=self.AGENT_MODULE,
            eval_dataset_file_path_or_dir=str(test_file),
            num_runs=1,
            agent_name="professor_virtual"
        )
    
    @pytest.mark.asyncio
    async def test_full_integration_flow(self):
        """Testa fluxo completo com captura de imagem e resposta."""
        test_file = Path(__file__).parent / "integration" / "full_flow.evalset.json"
        
        await AgentEvaluator.evaluate(
            agent_module=self.AGENT_MODULE,
            eval_dataset_file_path_or_dir=str(test_file),
            num_runs=1
        )
    
    @pytest.mark.asyncio
    async def test_all_unit_tests(self):
        """Executa todos os testes unitários."""
        unit_dir = Path(__file__).parent / "unit"
        
        await AgentEvaluator.evaluate(
            agent_module=self.AGENT_MODULE,
            eval_dataset_file_path_or_dir=str(unit_dir),
            num_runs=1,
            agent_name="professor_virtual"
        )
    
    @pytest.mark.asyncio
    async def test_all_integration_tests(self):
        """Executa todos os testes de integração."""
        integration_dir = Path(__file__).parent / "integration"
        
        await AgentEvaluator.evaluate(
            agent_module=self.AGENT_MODULE,
            eval_dataset_file_path_or_dir=str(integration_dir),
            num_runs=1
        )


@pytest.fixture
def mock_audio_data():
    """Fixture para dados de áudio simulados."""
    return "U2ltdWxhZG8gYXVkaW8gZGF0YQ=="  # "Simulado audio data" em base64


@pytest.fixture
def mock_image_data():
    """Fixture para dados de imagem simulados."""
    return "U2ltdWxhZG8gaW1hZ2VtIGRhdGE="  # "Simulado imagem data" em base64


def test_tools_exist():
    """Verifica se as ferramentas foram importadas corretamente."""
    try:
        from implementation import (
            transcrever_audio,
            analisar_necessidade_visual,
            analisar_imagem_educacional,
            gerar_audio_tts
        )
        assert callable(transcrever_audio)
        assert callable(analisar_necessidade_visual)
        assert callable(analisar_imagem_educacional)
        assert callable(gerar_audio_tts)
    except ImportError as e:
        pytest.fail(f"Falha ao importar ferramentas: {e}")


def test_instruction_providers_exist():
    """Verifica se os instruction providers foram criados."""
    try:
        from instruction_providers import (
            professor_instruction_provider,
            erro_instruction_provider,
            INSTRUCTION_PROVIDERS
        )
        assert callable(professor_instruction_provider)
        assert callable(erro_instruction_provider)
        assert len(INSTRUCTION_PROVIDERS) >= 6
    except ImportError as e:
        pytest.fail(f"Falha ao importar instruction providers: {e}")


# Para executar os testes:
# pytest tests/test_agent.py -v
# ou para um teste específico:
# pytest tests/test_agent.py::TestProfessorVirtualAgent::test_basic_questions -v
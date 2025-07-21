"""
Implementação das ferramentas customizadas para o Professor Virtual ADK
Todas as ferramentas seguem o padrão FunctionTool do Google ADK
"""

import re
import base64
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json

# Imports do ADK (conforme documentação)
from google.adk.tools import ToolContext


@dataclass
class AnaliseVisualResult:
    """Resultado da análise de necessidade visual"""
    necessita_imagem: bool
    confianca: float
    referencias_encontradas: list[str]


@dataclass
class AnaliseImagemResult:
    """Resultado da análise de imagem educacional"""
    tipo_conteudo: str  # exercicio, texto, diagrama, etc
    elementos_detectados: list[str]
    contexto_educacional: str
    qualidade_adequada: bool
    sugestao_acao: Optional[str]


async def transcrever_audio(
    audio_data: str,
    formato: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Transcreve arquivo de áudio completo para texto.
    
    Args:
        audio_data: Dados do áudio em base64
        formato: Formato do arquivo (wav, mp3, m4a)
        tool_context: Contexto da ferramenta ADK
        
    Returns:
        Dict contendo o texto transcrito e metadados
    """
    try:
        # Validar formato suportado
        formatos_suportados = ["wav", "mp3", "m4a"]
        if formato not in formatos_suportados:
            return {
                "erro": f"Formato {formato} não suportado",
                "sucesso": False
            }
        
        # Decodificar dados base64
        audio_bytes = base64.b64decode(audio_data)
        
        # Verificar tamanho máximo (10MB)
        max_size = 10 * 1024 * 1024
        if len(audio_bytes) > max_size:
            return {
                "erro": "Arquivo de áudio muito grande (máximo 10MB)",
                "sucesso": False
            }
        
        # NOTA: Em produção, aqui você integraria com um serviço real de STT
        # como Google Cloud Speech-to-Text, Whisper API, etc.
        # Por exemplo:
        # client = speech.SpeechClient()
        # response = client.recognize(config=config, audio=audio)
        
        # Simulação de transcrição para desenvolvimento
        texto_transcrito = "Este é um texto simulado da transcrição do áudio"
        duracao_segundos = len(audio_bytes) / (16000 * 2)  # Estimativa básica
        
        return {
            "sucesso": True,
            "texto": texto_transcrito,
            "duracao_segundos": duracao_segundos,
            "formato": formato,
            "tamanho_bytes": len(audio_bytes),
            "idioma_detectado": "pt-BR"
        }
        
    except Exception as e:
        return {
            "erro": f"Erro ao transcrever áudio: {str(e)}",
            "sucesso": False
        }


async def analisar_necessidade_visual(
    texto: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Analisa o texto transcrito para detectar referências que sugerem 
    necessidade de contexto visual.
    
    Args:
        texto: Texto transcrito da pergunta
        tool_context: Contexto da ferramenta ADK
        
    Returns:
        Dict com análise de necessidade visual
    """
    # Padrões que indicam referência visual
    padroes_visuais = [
        r'\b(esse|esta|esses|estas|aqui|aí|isso|isto)\b',
        r'\b(mostr\w+|ve[jr]|olh\w+|observ\w+)\b',
        r'\b(figura|imagem|foto|desenho|gráfico|diagrama|exercício|questão|problema)\b',
        r'\b(tá|está)\s+(escrito|mostrando|aparecendo)',
        r'o que (é|significa|quer dizer) (isso|isto)',
        r'não (entendi|compreendi) (esse|este|essa|esta)',
        r'(ajuda|me ajude|help) com (isso|este|esse)',
    ]
    
    texto_lower = texto.lower()
    referencias_encontradas = []
    pontuacao_visual = 0.0
    
    # Verificar cada padrão
    for padrao in padroes_visuais:
        matches = re.findall(padrao, texto_lower)
        if matches:
            referencias_encontradas.extend(matches)
            pontuacao_visual += len(matches) * 0.15
    
    # Análise de contexto adicional
    if "exercício" in texto_lower or "questão" in texto_lower:
        pontuacao_visual += 0.3
    
    if any(word in texto_lower for word in ["esse aqui", "esta aqui", "isso aqui"]):
        pontuacao_visual += 0.4
    
    # Normalizar pontuação
    confianca = min(pontuacao_visual, 1.0)
    necessita_imagem = confianca >= 0.5
    
    resultado = AnaliseVisualResult(
        necessita_imagem=necessita_imagem,
        confianca=confianca,
        referencias_encontradas=list(set(referencias_encontradas))
    )
    
    return {
        "necessita_imagem": resultado.necessita_imagem,
        "confianca": resultado.confianca,
        "referencias_encontradas": resultado.referencias_encontradas,
        "justificativa": f"Detectadas {len(resultado.referencias_encontradas)} referências visuais"
    }


async def analisar_imagem_educacional(
    imagem_data: str,
    contexto_pergunta: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Analisa imagem capturada extraindo informações educacionais relevantes.
    
    Args:
        imagem_data: Dados da imagem em base64
        contexto_pergunta: Contexto da pergunta original
        tool_context: Contexto da ferramenta ADK
        
    Returns:
        Dict com análise educacional da imagem
    """
    try:
        # Decodificar dados base64
        imagem_bytes = base64.b64decode(imagem_data)
        
        # Verificar tamanho máximo (5MB)
        max_size = 5 * 1024 * 1024
        if len(imagem_bytes) > max_size:
            return {
                "erro": "Imagem muito grande (máximo 5MB)",
                "sucesso": False,
                "qualidade_adequada": False
            }
        
        # NOTA: Em produção, aqui você integraria com um serviço real de visão
        # como Google Cloud Vision API, Azure Computer Vision, etc.
        # Também poderia usar Gemini Vision para análise educacional
        # Por exemplo:
        # vision_client = vision.ImageAnnotatorClient()
        # response = vision_client.analyze_image(image=image, features=features)
        
        # Simulação de análise para desenvolvimento
        resultado = AnaliseImagemResult(
            tipo_conteudo="exercicio_matematica",
            elementos_detectados=[
                "equação quadrática",
                "gráfico de parábola",
                "texto manuscrito",
                "números e símbolos matemáticos"
            ],
            contexto_educacional="Exercício de matemática sobre funções quadráticas",
            qualidade_adequada=True,
            sugestao_acao=None
        )
        
        # Verificar qualidade básica (simulada)
        if len(imagem_bytes) < 10000:  # Imagem muito pequena
            resultado.qualidade_adequada = False
            resultado.sugestao_acao = "Imagem pode estar com baixa resolução"
        
        return {
            "sucesso": True,
            "tipo_conteudo": resultado.tipo_conteudo,
            "elementos_detectados": resultado.elementos_detectados,
            "contexto_educacional": resultado.contexto_educacional,
            "qualidade_adequada": resultado.qualidade_adequada,
            "sugestao_acao": resultado.sugestao_acao,
            "tamanho_bytes": len(imagem_bytes),
            "contexto_pergunta": contexto_pergunta
        }
        
    except Exception as e:
        return {
            "erro": f"Erro ao analisar imagem: {str(e)}",
            "sucesso": False,
            "qualidade_adequada": False
        }


async def gerar_audio_tts(
    texto: str,
    velocidade: float = 1.0,
    voz: str = "pt-BR-Standard-A",
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Gera áudio TTS (Text-to-Speech) sob demanda para o texto fornecido.
    
    Args:
        texto: Texto para converter em áudio
        velocidade: Velocidade da fala (0.5 a 2.0)
        voz: Identificador da voz a usar
        tool_context: Contexto da ferramenta ADK
        
    Returns:
        Dict com dados do áudio gerado
    """
    try:
        # Validar parâmetros
        if not texto or len(texto.strip()) == 0:
            return {
                "erro": "Texto vazio fornecido",
                "sucesso": False
            }
        
        if velocidade < 0.5 or velocidade > 2.0:
            velocidade = 1.0
        
        # Limitar tamanho do texto (evitar textos muito longos)
        max_chars = 5000
        if len(texto) > max_chars:
            texto = texto[:max_chars] + "..."
        
        # NOTA: Em produção, aqui você integraria com um serviço real de TTS
        # como Google Cloud Text-to-Speech, Amazon Polly, Azure Speech, etc.
        # Por exemplo:
        # tts_client = texttospeech.TextToSpeechClient()
        # synthesis_input = texttospeech.SynthesisInput(text=texto)
        # voice = texttospeech.VoiceSelectionParams(...)
        # audio_config = texttospeech.AudioConfig(...)
        # response = tts_client.synthesize_speech(...)
        
        # Simulação de geração de áudio para desenvolvimento
        # Em produção, isso seria o áudio real em base64
        audio_simulado_base64 = base64.b64encode(b"audio_data_simulado").decode()
        duracao_estimada = len(texto.split()) / 150 * 60  # ~150 palavras por minuto
        
        return {
            "sucesso": True,
            "audio_base64": audio_simulado_base64,
            "formato": "mp3",
            "duracao_segundos": duracao_estimada,
            "velocidade": velocidade,
            "voz": voz,
            "tamanho_caracteres": len(texto),
            "tamanho_bytes": len(audio_simulado_base64)
        }
        
    except Exception as e:
        return {
            "erro": f"Erro ao gerar áudio TTS: {str(e)}",
            "sucesso": False
        }


# Funções auxiliares para validação e processamento

def validar_audio_metadata(metadata: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Valida metadados do áudio antes do processamento"""
    if "formato" not in metadata:
        return False, "Formato do áudio não especificado"
    
    if "tamanho_bytes" in metadata and metadata["tamanho_bytes"] > 10 * 1024 * 1024:
        return False, "Arquivo muito grande"
    
    return True, None


def extrair_contexto_educacional(texto: str) -> Dict[str, Any]:
    """Extrai contexto educacional do texto para melhor processamento"""
    materias = {
        "matematica": ["conta", "número", "equação", "calcul", "soma", "multiplicação"],
        "portugues": ["palavra", "frase", "texto", "verbo", "substantivo", "letra"],
        "ciencias": ["animal", "planta", "corpo", "natureza", "experimento"],
        "historia": ["ano", "época", "aconteceu", "passado", "história"],
        "geografia": ["país", "cidade", "mapa", "continente", "oceano"]
    }
    
    texto_lower = texto.lower()
    materia_detectada = "geral"
    
    for materia, palavras_chave in materias.items():
        if any(palavra in texto_lower for palavra in palavras_chave):
            materia_detectada = materia
            break
    
    return {
        "materia_provavel": materia_detectada,
        "nivel_complexidade": "basico",  # Pode ser expandido com análise mais sofisticada
        "tipo_ajuda": "explicacao"  # explicacao, resolucao, dica, etc.
    }


# Registro das ferramentas para uso com o ADK
PROFESSOR_TOOLS = {
    "transcrever_audio": transcrever_audio,
    "analisar_necessidade_visual": analisar_necessidade_visual,
    "analisar_imagem_educacional": analisar_imagem_educacional,
    "gerar_audio_tts": gerar_audio_tts
}
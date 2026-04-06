import pytest
from unittest.mock import patch, mock_open, call
import sys
import os

# Añadir src al path para poder importar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from researcher import run_research_agent


def test_run_research_agent_single_call():
    """Prueba que el agente investigador funcione correctamente con 1 iteración."""
    
    mock_config = {
        'dynamic_instructions': {'current_research_focus': 'Un misterio en marte'},
        'system_settings': {'temperature_research': 0.8, 'researcher_calls_per_run': 1},
        'genres': [{'name': 'Sci-Fi', 'weight': 100}]
    }

    m_open = mock_open()
    
    with patch('researcher.load_config', return_value=mock_config), \
         patch('researcher.get_active_genres', return_value=[{'name': 'Sci-Fi', 'weight': 100}]), \
         patch('researcher.format_genre_weights', return_value="Sci-Fi: 100%"), \
         patch('researcher.call_ai_api', return_value="Idea 1 mock") as mock_call_ai, \
         patch("builtins.open", m_open):
        
        run_research_agent()
        
    # Verificaciones
    assert mock_call_ai.call_count == 1
    # Verifica que el archivo de log fue abierto en modo append
    m_open.assert_called_with('../data/research_log.txt', 'a', encoding='utf-8')
    # Verifica que se escribió el resultado
    handle = m_open()
    handle.write.assert_any_call('\n--- ITERACIÓN 1 ---\nIdea 1 mock\n')


def test_run_research_agent_multiple_calls():
    """Prueba que el agente itere correctamente N veces si está configurado."""
    
    mock_config = {
        'dynamic_instructions': {'current_research_focus': 'Un misterio'},
        'system_settings': {'temperature_research': 0.8, 'researcher_calls_per_run': 3},
        'genres': [{'name': 'Sci-Fi', 'weight': 100}]
    }

    m_open = mock_open()
    mock_responses = ["Respuesta 1", "Respuesta 2", "Respuesta 3"]
    
    with patch('researcher.load_config', return_value=mock_config), \
         patch('researcher.get_active_genres', return_value=[{'name': 'Sci-Fi', 'weight': 100}]), \
         patch('researcher.format_genre_weights', return_value="Sci-Fi: 100%"), \
         patch('researcher.call_ai_api', side_effect=mock_responses) as mock_call_ai, \
         patch("builtins.open", m_open):
        
        run_research_agent()
        
    assert mock_call_ai.call_count == 3
    
    # Validamos que iteró llamando al write por cada respuesta
    handle = m_open()
    handle.write.assert_has_calls([
        call('\n--- ITERACIÓN 1 ---\nRespuesta 1\n'),
        call('\n--- ITERACIÓN 2 ---\nRespuesta 2\n'),
        call('\n--- ITERACIÓN 3 ---\nRespuesta 3\n')
    ], any_order=False)


def test_run_research_agent_api_error():
    """Prueba que los errores en la API propaguen o logueen adecuadamente."""

    mock_config = {
        'dynamic_instructions': {'current_research_focus': 'Misterio'},
        'system_settings': {'temperature_research': 0.8, 'researcher_calls_per_run': 1},
    }

    with patch('researcher.load_config', return_value=mock_config), \
         patch('researcher.get_active_genres', return_value=[]), \
         patch('researcher.format_genre_weights', return_value="Ninguno"), \
         patch('researcher.call_ai_api', side_effect=Exception("API MOCK ERROR")), \
         patch("builtins.open", mock_open()):
        
        with pytest.raises(Exception, match="API MOCK ERROR"):
            run_research_agent()

import os
import json
from unittest.mock import patch, mock_open, MagicMock
from src.writer import generate_chapter_summary, run_writing_agent

def test_generate_chapter_summary():
    config = {"story_status": {"title": "Test Novel"}}
    chapter_content = "Había una vez un test."
    chapter_num = 1
    
    with patch("src.writer.call_ai_api", return_value="Este es un resumen."):
        summary = generate_chapter_summary(chapter_content, chapter_num, config)
        assert summary == "Este es un resumen."

@patch("src.writer.call_ai_api")
@patch("src.writer.load_config")
@patch("src.writer.save_config")
def test_run_writing_agent_success(mock_save, mock_load, mock_call):
    # Setup mocks
    mock_load.return_value = {
        "story_status": {
            "title": "Test Novel",
            "last_chapter_number": 0,
            "target_chapter_words": 500
        },
        "system_settings": {
            "temperature_writing": 0.7,
            "max_tokens_output": 1000
        },
        "dynamic_instructions": {
            "writing_style_override": "Test style"
        },
        "genre_weights": {"action": 100}
    }
    
    # Mock calls: 1 for chapter, 1 for summary
    mock_call.side_effect = ["Contenido del capítulo", "Resumen del capítulo"]
    
    # Mock file operations
    with patch("src.writer.read_file", return_value="Contexto previo"), \
         patch("builtins.open", mock_open()) as mocked_file:
        
        run_writing_agent()
        
        # Verify chapter save
        # Cap 0 + 1 = Cap 1
        mocked_file.assert_any_call("../chapters/cap_001.md", 'w', encoding='utf-8')
        
        # Verify resúmenes.md append
        mocked_file.assert_any_call('../data/resúmenes.md', 'a', encoding='utf-8')
        
        # Verify research_log.txt clear
        mocked_file.assert_any_call('../data/research_log.txt', 'w', encoding='utf-8')
        
        # Verify config update
        assert mock_save.called
        updated_config = mock_save.call_args[0][0]
        assert updated_config['story_status']['last_chapter_number'] == 1

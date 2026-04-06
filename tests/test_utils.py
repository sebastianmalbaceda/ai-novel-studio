import os
import json
from unittest.mock import patch, mock_open, MagicMock
from src.utils import load_config, get_active_genres, format_genre_weights, call_ai_api

def test_load_config():
    fake_config = '{"system_settings": {"api_provider": "minimax"}}'
    with patch("builtins.open", mock_open(read_data=fake_config)):
        config = load_config()
        assert config["system_settings"]["api_provider"] == "minimax"

def test_get_active_genres():
    config = {
        "genre_weights": {
            "_comment": "test",
            "rom_com": 40,
            "action": 0,
            "sci_fi": 15
        }
    }
    active = get_active_genres(config)
    assert active == {"rom_com": 40, "sci_fi": 15}

def test_format_genre_weights():
    genres = {"rom_com": 40, "sci_fi": 15}
    formatted = format_genre_weights(genres)
    assert "- Rom Com: 40%" in formatted
    assert "- Sci Fi: 15%" in formatted

@patch("src.utils.requests.post")
@patch.dict(os.environ, {"AI_API_KEY": "test-key"})
def test_call_ai_api_success(mock_post):
    fake_config = {
        "system_settings": {
            "api_host": "https://fake.api/v1/chat/completions",
            "model_name": "fake-model",
            "api_key_env": "AI_API_KEY",
            "extra_headers": {"X-Custom": "test"},
            "extra_body_params": {"stream": False}
        }
    }
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Respuesta generada"}}]
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    with patch("src.utils.load_config", return_value=fake_config):
        result = call_ai_api("Prueba")
        assert result == "Respuesta generada"

        # Check call arguments
        args, kwargs = mock_post.call_args
        assert args[0] == "https://fake.api/v1/chat/completions"
        assert kwargs["headers"]["X-Custom"] == "test"
        assert kwargs["headers"]["Authorization"] == "Bearer test-key"
        assert kwargs["json"]["model"] == "fake-model"
        assert kwargs["json"]["stream"] is False

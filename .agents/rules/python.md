# Reglas de Python — A.I. Novel Studio

## Encoding
- SIEMPRE usar `encoding='utf-8'` al abrir archivos
- JSON: `ensure_ascii=False` en `json.dump()`

## API Calls
- SIEMPRE usar `utils.call_ai_api()` — nunca `requests.post()` directo
- Las API Keys se leen de `os.environ.get("MINIMAX_API_KEY")`
- Manejar `response.raise_for_status()` con try/except

## Paths
- Todas las rutas son relativas desde `src/` (e.g., `../data/config.json`)
- NUNCA usar rutas absolutas
- Usar `os.path.exists()` antes de leer archivos opcionales

## Config
- Parámetros dinámicos en `data/config.json` — no hardcodear
- Leer config con `utils.load_config()`
- Guardar config con `utils.save_config()`

## Estilo
- PEP 8, máximo 100 caracteres por línea
- Docstrings Google style
- Variables en inglés, strings de usuario en español
- Type hints opcionales pero recomendados

## Testing
- Framework: pytest
- Mockear APIs y file I/O
- No tests que dependan de red

## Imports
```python
# 1. Standard library
import os
import json

# 2. Third-party
import requests

# 3. Local
from utils import load_config, call_ai_api
```

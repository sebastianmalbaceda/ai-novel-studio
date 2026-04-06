---
name: generate-tests
description: |
  Genera tests unitarios con pytest para los módulos Python del proyecto
  (utils.py, researcher.py, writer.py). Activar cuando se soliciten tests,
  se modifiquen funciones existentes, o se añadan funciones nuevas.
  No activar para cambios puramente documentales.
---

# Instrucciones: Generación de Tests

## Framework y Herramientas

- **Test runner:** pytest
- **Mocking:** unittest.mock (Mock, patch, MagicMock)
- **Directorio de tests:** `tests/`
- **Naming:** `test_<module_name>.py`

## Convenciones

1. **NUNCA** hacer llamadas reales a APIs externas en tests
2. Mockear siempre `utils.call_ai_api()` y `requests.post`
3. Mockear operaciones de archivos con `mock_open` o `tmp_path`
4. Cada test debe ser independiente y no depender del orden de ejecución
5. Usar `assert` statements claros con mensajes descriptivos

## Estructura de un Test

```python
import pytest
from unittest.mock import patch, mock_open

def test_function_name_happy_path():
    """Descripción de qué se está testeando."""
    # Arrange
    mock_data = {...}
    
    # Act
    with patch('module.dependency', return_value=mock_data):
        result = function_under_test()
    
    # Assert
    assert result == expected_value
```

## Ejecución

```bash
# Todos los tests
python -m pytest tests/

# Test específico
python -m pytest tests/test_utils.py -v

# Con cobertura
python -m pytest tests/ --cov=src/
```

## Cobertura Mínima

- `utils.py`: ≥ 80%
- `researcher.py`: ≥ 70%
- `writer.py`: ≥ 70%

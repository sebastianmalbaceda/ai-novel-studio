# Testing Strategy — A.I. Novel Studio

## Framework

- **Test runner:** pytest
- **Mocking:** unittest.mock
- **Directorio:** `tests/`

## Categorías de Tests

### Tests Unitarios

| Módulo | Archivo de Test | Cobertura Objetivo |
|--------|----------------|-------------------|
| `src/utils.py` | `tests/test_utils.py` | ≥ 80% |
| `src/researcher.py` | `tests/test_researcher.py` | ≥ 70% |
| `src/writer.py` | `tests/test_writer.py` | ≥ 70% |

### Principios

1. **Aislamiento:** Cada test es independiente. No depende del orden de ejecución.
2. **No network:** NUNCA hacer llamadas reales a APIs en tests.
3. **Mocking:** Usar `unittest.mock.patch` para mockear `call_ai_api()` y `requests.post`.
4. **File I/O:** Usar `mock_open` o `tmp_path` para operaciones de archivo.
5. **Idempotencia:** Los tests deben poder ejecutarse múltiples veces con el mismo resultado.

## Ejecución

```bash
# Todos los tests
python -m pytest tests/ -v

# Test específico
python -m pytest tests/test_utils.py -v

# Con cobertura
python -m pytest tests/ --cov=src/ --cov-report=term-missing
```

## Estructura de Tests

```python
def test_function_happy_path():
    """Test del caso exitoso."""
    # Arrange
    # Act
    # Assert

def test_function_error_handling():
    """Test del manejo de errores."""
    # Arrange
    # Act & Assert (pytest.raises)
```

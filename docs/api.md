# API Reference — A.I. Novel Studio

> **Versión:** 1.0.0  
> **Última actualización:** 2026-04-06

---

## Módulo `src/utils.py`

### `load_config() → dict`

Lee el archivo de configuración dinámica del proyecto.

**Retorna:** Diccionario con la configuración completa de `data/config.json`.

**Excepciones:**
- `FileNotFoundError`: Si `data/config.json` no existe.
- `json.JSONDecodeError`: Si el archivo tiene formato JSON inválido.

**Ejemplo:**
```python
config = load_config()
print(config['story_status']['title'])
```

---

### `save_config(config_data: dict) → None`

Guarda actualizaciones en el archivo de configuración.

**Parámetros:**
- `config_data` (dict): Diccionario completo de configuración.

**Ejemplo:**
```python
config = load_config()
config['story_status']['last_chapter_number'] = 5
save_config(config)
```

---

### `call_ai_api(prompt, system_prompt, temperature, max_tokens) → str`

Realiza una llamada genérica a la API del modelo de IA.

**Parámetros:**
- `prompt` (str): Texto del prompt del usuario.
- `system_prompt` (str, default: "Eres un útil asistente de escritura."): Prompt de sistema.
- `temperature` (float, default: 0.7): Nivel de creatividad (0.0 a 1.0).
- `max_tokens` (int, default: 2000): Límite de tokens en la respuesta.

**Retorna:** String con el contenido generado por la IA.

**Excepciones:**
- `ValueError`: Si la API Key no está configurada (variable definida en `config.json → api_key_env`).
- `requests.exceptions.HTTPError`: Si la petición HTTP falla.

**Ejemplo:**
```python
response = call_ai_api(
    prompt="Genera 3 ideas para un giro de trama",
    system_prompt="Eres un experto en narrativa",
    temperature=0.8,
    max_tokens=1000
)
```

---

## Módulo `src/researcher.py`

### `run_research_agent() → None`

Ejecuta el ciclo completo del agente investigador:
1. Lee configuración
2. Construye prompt de investigación basado en pesos de género
3. Llama a la API de IA
4. Añade resultados a `data/research_log.txt` (append mode)

**Trigger:** GitHub Actions cada 15 minutos.

---

## Módulo `src/writer.py`

### `read_file(filepath: str) → str`

Lee un archivo de texto, retorna string vacío si no existe.

**Parámetros:**
- `filepath` (str): Ruta al archivo.

**Retorna:** Contenido del archivo o string vacío.

---

### `run_writing_agent() → None`

Ejecuta el ciclo completo del agente escritor:
1. Lee biblia, resúmenes y log de investigación
2. Construye mega-prompt
3. Genera capítulo
4. Guarda como `chapters/cap_XXX.md`
5. Actualiza `last_chapter_number` en config
6. Vacía `research_log.txt`

**Trigger:** GitHub Actions cada hora.

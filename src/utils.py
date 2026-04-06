import os
import json
import requests


def load_config():
    """Lee el archivo de configuración con los parámetros dinámicos."""
    with open('../data/config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config_data):
    """Guarda actualizaciones en el archivo de configuración."""
    with open('../data/config.json', 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=4, ensure_ascii=False)


def get_active_genres(config):
    """
    Extrae los géneros activos (peso > 0) del config.
    Ignora las claves de separación (prefijo '___' o '_comment').

    Returns:
        dict: Diccionario {nombre_genero: peso} solo para géneros con peso > 0.
    """
    genres = {}
    for key, value in config.get('genre_weights', {}).items():
        # Ignorar separadores de categoría y comentarios
        if key.startswith('_'):
            continue
        if isinstance(value, (int, float)) and value > 0:
            genres[key] = value
    return genres


def format_genre_weights(genres):
    """
    Formatea los géneros activos como texto legible para inyectar en prompts.

    Args:
        genres: dict con {nombre: peso} de géneros activos.

    Returns:
        str: Texto formateado con los géneros y sus pesos.
    """
    if not genres:
        return "No hay géneros con peso definido."
    
    lines = []
    for name, weight in sorted(genres.items(), key=lambda x: x[1], reverse=True):
        display_name = name.replace('_', ' ').title()
        lines.append(f"- {display_name}: {weight}%")
    return "\n".join(lines)


def call_ai_api(prompt, system_prompt="Eres un útil asistente de escritura.", temperature=0.7, max_tokens=2000):
    """
    Realiza la llamada genérica a cualquier API compatible con el formato OpenAI.
    Soporta cualquier proveedor (Minimax, OpenAI, Anthropic-compatible, 
    DeepSeek, Groq, Mistral, local, etc.) configurado en data/config.json.

    La función lee del config:
      - api_host: URL completa del endpoint (ej: https://api.minimax.io/v1/chat/completions)
      - api_key_env: Nombre de la variable de entorno que contiene la API Key
      - model_name: Nombre del modelo a usar
      - extra_headers: Headers adicionales (dict)
      - extra_body_params: Parámetros extra para el body (dict)

    Args:
        prompt: El texto del prompt del usuario.
        system_prompt: El prompt de sistema para configurar el comportamiento.
        temperature: Nivel de creatividad (0.0-1.0).
        max_tokens: Máximo de tokens en la respuesta.

    Returns:
        str: El contenido de texto generado por la IA.

    Raises:
        ValueError: Si la API Key no está configurada en las variables de entorno.
        requests.exceptions.HTTPError: Si la petición HTTP falla.
    """
    config = load_config()
    settings = config['system_settings']

    # Leer el nombre de la variable de entorno para la API Key
    api_key_env = settings.get('api_key_env', 'AI_API_KEY')
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise ValueError(
            f"La API Key no está configurada. "
            f"Define la variable de entorno '{api_key_env}' con tu clave. "
            f"En GitHub: Settings → Secrets → New → {api_key_env}"
        )

    # URL del endpoint — completamente configurable
    url = settings.get('api_host', 'https://api.minimax.io/v1/chat/completions')
    model_name = settings.get('model_name', 'MiniMax-M1')

    # Headers base + extras configurables
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    extra_headers = settings.get('extra_headers', {})
    if extra_headers:
        headers.update(extra_headers)

    # Payload base formato OpenAI-compatible
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # Parámetros extra del body (útil para proveedores con opciones especiales)
    extra_body = settings.get('extra_body_params', {})
    if extra_body:
        payload.update(extra_body)

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error en la llamada a la API ({settings.get('api_provider', 'unknown')}): {e.response.text}")
        else:
            print(f"Error en la llamada a la API ({settings.get('api_provider', 'unknown')}): {e}")
        raise

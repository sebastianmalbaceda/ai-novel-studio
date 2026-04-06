# Documentación Técnica: Proyecto "A.I. Novel Studio" (Estudio Autónomo de Novelas Ligeras)

## 1. Visión General del Proyecto
"A.I. Novel Studio" es un sistema de generación automatizada de literatura (Novelas Ligeras, Webnovels, Mangas) impulsado por modelos de Inteligencia Artificial (LLMs). Está diseñado para operar de forma 100% autónoma y gratuita utilizando **GitHub Actions** como motor de ejecución (orquestador). 

El objetivo principal del sistema no es solo generar texto, sino **investigar intensivamente** para enriquecer la trama, agilizar giros argumentales y maximizar el uso de contexto ("quema de tokens"). Utiliza un flujo asíncrono donde múltiples "Agentes Investigadores" recopilan información, tropos, datos históricos y de ciencia ficción periódicamente, para que posteriormente un "Agente Escritor" compile todo y publique un capítulo nuevo de forma horaria.

## 2. Arquitectura del Sistema


El sistema se divide en tres capas fundamentales que interactúan dentro del repositorio de GitHub:

* **Capa de Almacenamiento (El Repositorio):** GitHub actúa como la base de datos central. Guarda la "Biblia" (reglas del mundo), el historial de investigación en caché, la configuración de parámetros y los capítulos finales publicados.
* **Capa de Ejecución (GitHub Actions):** Máquinas virtuales efímeras que se levantan mediante tareas *cron*. Ejecutan los scripts de Python de forma calendarizada sin necesidad de mantener un servidor dedicado encendido.
* **Capa Cognitiva (APIs de IA):** La conexión externa hacia Minimax (u otros modelos gratuitos/alternativos en el futuro). Se alimenta de variables de entorno protegidas a través de GitHub Secrets, garantizando la seguridad de las API Keys.

## 3. Ciclo de Vida y Flujo de Trabajo (El Bucle)

El proyecto implementa un ciclo de dos velocidades para garantizar profundidad narrativa y un alto consumo de tokens justificado:

1.  **Fase de Recopilación (Ejecución cada 15 minutos):**
    * Un flujo de trabajo de GitHub Actions ejecuta un script secundario (`researcher.py`).
    * La IA recibe instrucciones basadas en los parámetros actuales para investigar sobre la trama, buscar tropos en internet (Sci-Fi, Rom-com, Acción), explorar posibles giros argumentales o planificar el desarrollo de personajes.
    * Los resultados de estas llamadas continuas se procesan y se añaden a un archivo de texto en bruto (`research_log.txt`) dentro del repositorio.
2.  **Fase de Síntesis y Publicación (Ejecución cada 1 hora):**
    * Un flujo de trabajo principal ejecuta el script de redacción (`writer.py`).
    * Se inyecta un *Mega-Prompt* a la IA que contiene: La Biblia de la novela + El resumen de los últimos capítulos + **Todo el contenido de `research_log.txt` acumulado**.
    * La IA redacta el capítulo final asegurando la continuidad narrativa, lo formatea en Markdown, vacía el archivo `research_log.txt` para el siguiente ciclo, y ejecuta un `git commit` y `git push` automáticos del nuevo capítulo a la rama principal.

## 4. Estructura de Directorios del Repositorio

Para construir el proyecto, el repositorio deberá contener exactamente la siguiente jerarquía de archivos y carpetas:

```text
AI-Novel-Studio/
├── .github/
│   └── workflows/
│       ├── cron_researcher.yml    # Acción que se ejecuta cada 15 min
│       └── cron_writer.yml        # Acción que se ejecuta cada 1 hora
├── src/
│   ├── researcher.py              # Lógica del Agente Investigador
│   ├── writer.py                  # Lógica del Agente Escritor
│   └── utils.py                   # Funciones compartidas (Llamadas API, operaciones Git)
├── data/
│   ├── config.json                # Panel de control de parámetros dinámicos
│   ├── biblia.md                  # Fichas de personajes, reglas del mundo, lore
│   ├── resúmenes.md               # Resumen condensado de la historia hasta el momento
│   └── research_log.txt           # Archivo temporal que acumula investigaciones
├── chapters/                      # Directorio de salida para la novela
│   ├── cap_001.md
│   └── cap_002.md
├── requirements.txt               # Dependencias de Python (ej. requests)
└── README.md                      # Portada y sinopsis del proyecto público
```

## 5. El Panel de Control (`data/config.json`)

Para mantener un control paramétrico absoluto sobre la dirección de la historia sin tener que tocar el código fuente de los scripts, el sistema leerá este archivo en cada ejecución. Esto permite inyectar giros argumentales o cambiar el comportamiento de la IA sobre la marcha.

```json
{
  "system_settings": {
    "api_provider": "minimax",
    "model_name": "minimax-v1",
    "max_tokens_output": 3000,
    "temperature_research": 0.8,
    "temperature_writing": 0.65
  },
  "story_status": {
    "title": "El título de tu novela",
    "current_arc": "Introducción y descubrimiento del misterio principal",
    "target_chapter_words": 1500,
    "last_chapter_number": 2
  },
  "genre_weights": {
    "rom_com": 40,
    "action": 25,
    "sci_fi": 15,
    "mystery": 10,
    "slice_of_life": 10
  },
  "dynamic_instructions": {
    "current_research_focus": "Busca ideas sobre cómo combinar tropos de invasiones alienígenas con malentendidos románticos de instituto.",
    "writing_style_override": "Mantén diálogos ágiles, humor absurdo y descripciones detalladas durante las escenas de acción (estilo shounen/seinen)."
  }
}
```

[FIN DE LA PARTE 1 - Escribe "continua" para generar la Parte 2: Lógica de los Agentes en Python (researcher.py, writer.py y utils.py) y gestión de la API.]

## 6. Funciones Compartidas y Conexión API (`src/utils.py`)

Este archivo contiene las herramientas fundamentales para que el sistema funcione. Se encarga de la lectura de configuraciones, el manejo seguro de la API Key mediante variables de entorno y las llamadas al modelo de Inteligencia Artificial.

```python
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

def call_ai_api(prompt, system_prompt="Eres un útil asistente de escritura.", temperature=0.7, max_tokens=2000):
    """
    Realiza la llamada genérica a la API del modelo (ej. Minimax).
    Requiere que la variable de entorno MINIMAX_API_KEY esté configurada.
    """
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("La API Key no está configurada en las variables de entorno.")

    # NOTA: Esta URL y estructura de payload dependen de la documentación oficial de Minimax
    # Este es un formato estándar compatible con muchas APIs tipo OpenAI.
    url = "https://api.minimax.chat/v1/text/chatcompletion" 
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "minimax-v1", # Nombre del modelo configurado
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Lanza error si la petición falla
    
    data = response.json()
    return data['choices'][0]['message']['content']
```

## 7. El Agente Investigador (`src/researcher.py`)

Este script es el responsable de "quemar tokens" productivamente. Se ejecuta varias veces por hora para hacer brainstorming, investigar tropos y dejar notas preparadas para el escritor principal.

```python
import os
from utils import load_config, call_ai_api

def run_research_agent():
    config = load_config()
    research_focus = config['dynamic_instructions']['current_research_focus']
    temp = config['system_settings']['temperature_research']
    
    system_prompt = "Eres un investigador experto en tropos literarios, ciencia ficción y manga."
    
    prompt = f"""
    Realiza una investigación y lluvia de ideas sobre el siguiente tema:
    "{research_focus}"
    
    Busca formas originales de integrar estos elementos en una historia que combina:
    Rom-Com ({config['genre_weights']['rom_com']}% de peso)
    Acción ({config['genre_weights']['action']}% de peso)
    Sci-Fi ({config['genre_weights']['sci_fi']}% de peso)
    
    Genera 3 ideas concretas (eventos, revelaciones de misterio o interacciones entre personajes).
    Devuelve solo el texto de tus ideas, estructurado en puntos.
    """
    
    print("Iniciando investigación...")
    research_output = call_ai_api(prompt, system_prompt, temperature=temp)
    
    # Añadir el resultado al archivo log (append mode)
    with open('../data/research_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n\n--- INFORME DE INVESTIGACIÓN ---\n{research_output}\n")
        
    print("Investigación completada y guardada en research_log.txt")

if __name__ == "__main__":
    run_research_agent()
```

## 8. El Agente Escritor (`src/writer.py`)

Este es el núcleo del proyecto. Se ejecuta una vez por hora. Toma toda la información, la Biblia de la historia y las notas del investigador para redactar el capítulo final.

```python
import os
from utils import load_config, save_config, call_ai_api

def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def run_writing_agent():
    config = load_config()
    
    # Leer contexto
    biblia = read_file('../data/biblia.md')
    resumen = read_file('../data/resúmenes.md')
    research_notes = read_file('../data/research_log.txt')
    
    chapter_num = config['story_status']['last_chapter_number'] + 1
    temp = config['system_settings']['temperature_writing']
    max_tokens = config['system_settings']['max_tokens_output']
    style = config['dynamic_instructions']['writing_style_override']
    
    system_prompt = "Eres un aclamado autor de novelas ligeras especializadas en mezclar Rom-com, Acción y Sci-Fi."
    
    mega_prompt = f"""
    Vas a escribir el CAPÍTULO {chapter_num} de la novela "{config['story_status']['title']}".
    
    [REGLAS DEL MUNDO Y PERSONAJES (BIBLIA)]
    {biblia}
    
    [RESUMEN DE LA HISTORIA HASTA AHORA]
    {resumen}
    
    [NOTAS DE INVESTIGACIÓN (USA ESTAS IDEAS PARA EL CAPÍTULO DE HOY)]
    {research_notes}
    
    [INSTRUCCIONES DE ESTILO]
    {style}
    El capítulo debe tener aproximadamente {config['story_status']['target_chapter_words']} palabras.
    Mantén un equilibrio donde el Rom-Com es la base de las interacciones, pero el misterio Sci-Fi y la acción avanzan la trama.
    
    Escribe directamente el capítulo en formato Markdown.
    """
    
    print(f"Redactando Capítulo {chapter_num}...")
    chapter_content = call_ai_api(mega_prompt, system_prompt, temperature=temp, max_tokens=max_tokens)
    
    # Guardar el capítulo
    chapter_filename = f"../chapters/cap_{chapter_num:03d}.md"
    with open(chapter_filename, 'w', encoding='utf-8') as f:
        f.write(f"# Capítulo {chapter_num}\n\n{chapter_content}")
        
    print(f"Capítulo {chapter_num} guardado con éxito.")
    
    # Actualizar estado en config.json
    config['story_status']['last_chapter_number'] = chapter_num
    save_config(config)
    
    # Limpiar el registro de investigación para el siguiente ciclo horario
    with open('../data/research_log.txt', 'w', encoding='utf-8') as f:
        f.write("")
        
if __name__ == "__main__":
    run_writing_agent()
```

[FIN DE LA PARTE 2 - Escribe "continua" para generar la Parte 3 y final: Archivos de orquestación en GitHub Actions (.yml) y configuración para automatizar los Git Commits.]

## 9. Orquestación: GitHub Actions (El Motor)

Para que el proyecto se ejecute de forma autónoma sin que tu ordenador esté encendido, utilizaremos los "Workflows" de GitHub. Estos archivos `.yml` le dicen a los servidores de GitHub cuándo ejecutar los scripts y cómo guardar los cambios (Commits).

### Archivo 1: El Investigador (`.github/workflows/cron_researcher.yml`)
Este flujo de trabajo levanta una máquina virtual cada 15 minutos, ejecuta el script de investigación y guarda las nuevas ideas en el archivo de registro.

```yaml
name: Agente Investigador (Cada 15 min)

on:
  schedule:
    # Se ejecuta en el minuto 0, 15, 30 y 45 de cada hora
    - cron: '*/15 * * * *'
  workflow_dispatch: # Permite ejecutarlo manualmente desde la web de GitHub

jobs:
  run-research:
    runs-on: ubuntu-latest
    
    steps:
      - name: Descargar el repositorio
        uses: actions/checkout@v3

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Ejecutar investigador
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
        run: |
          cd src
          python researcher.py

      - name: Hacer commit y push del registro de investigación
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add data/research_log.txt
          # Solo hace commit si hay cambios reales
          git diff --quiet && git diff --staged --quiet || git commit -m "🤖 AI Log: Nueva investigación añadida"
          git push
```

### Archivo 2: El Escritor (`.github/workflows/cron_writer.yml`)
Este flujo se ejecuta una vez cada hora. Toma la investigación acumulada, escribe el capítulo definitivo y lo sube al repositorio para que puedas leerlo.

```yaml
name: Agente Escritor (Cada Hora)

on:
  schedule:
    # Se ejecuta en el minuto 0 de cada hora
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  write-chapter:
    runs-on: ubuntu-latest
    
    steps:
      - name: Descargar el repositorio
        uses: actions/checkout@v3

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Ejecutar escritor
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
        run: |
          cd src
          python writer.py

      - name: Hacer commit y push del nuevo capítulo y actualizar estado
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add chapters/ data/config.json data/research_log.txt
          git diff --quiet && git diff --staged --quiet || git commit -m "📖 AI Release: Nuevo capítulo publicado"
          git push
```

## 10. Configuración Final en GitHub (IMPORTANTE)

Una vez hayas subido todo tu código al repositorio de GitHub, necesitas realizar dos ajustes críticos en la configuración web de tu repositorio para que la magia funcione:

**Paso 1: Proteger tu API Key (Los Secrets)**
1. Ve a la pestaña **Settings** de tu repositorio en GitHub.
2. En el menú lateral izquierdo, baja hasta **Secrets and variables** y haz clic en **Actions**.
3. Haz clic en el botón verde **New repository secret**.
4. En el campo "Name", escribe exactamente: `MINIMAX_API_KEY`
5. En el campo "Secret", pega tu clave secreta de la API.
6. Haz clic en "Add secret". Ahora la clave está cifrada y tu código puede usarla sin exponerla.

**Paso 2: Dar permisos de escritura al Bot**
Por defecto, GitHub Actions no tiene permiso para modificar tus archivos (como guardar los nuevos capítulos). Tienes que darle permiso explícito:
1. Ve a la pestaña **Settings** de tu repositorio.
2. En el menú lateral izquierdo, haz clic en **Actions** > **General**.
3. Baja hasta la sección que dice **Workflow permissions**.
4. Selecciona la opción **Read and write permissions**.
5. Haz clic en **Save**.

## 11. ¿Cómo consumir tu novela?
¡El sistema ya es autónomo! A partir de este momento:
* Puedes entrar a la carpeta `chapters/` de tu repositorio desde el móvil o el PC para leer el avance en formato Markdown (`.md`).
* Si la historia se desvía, simplemente edita manualmente el archivo `data/config.json` en GitHub, cambia el `current_research_focus` o los pesos de los géneros, haz commit, y la IA tomará esa nueva dirección en la siguiente hora.

[FIN DE LA DOCUMENTACIÓN]
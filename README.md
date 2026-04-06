# 📖 A.I. Novel Studio

> **Sistema autónomo de generación de Novelas Ligeras impulsado por Inteligencia Artificial**

[![GitHub Actions](https://img.shields.io/badge/Orquestado%20por-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/Licencia-MIT-green.svg)](LICENSE)
[![AI Powered](https://img.shields.io/badge/IA-Multi--Model-FF6B35?logo=openai&logoColor=white)](#)

---

## 🎯 ¿Qué es A.I. Novel Studio?

**A.I. Novel Studio** es un sistema de generación automatizada de literatura (Novelas Ligeras, Webnovels, Mangas) que opera de forma **100% autónoma y gratuita** utilizando GitHub Actions como motor de ejecución.

El sistema no solo genera texto — **investiga intensivamente** para enriquecer la trama, diversificar giros argumentales y maximizar la calidad narrativa a través de un flujo asíncrono de dos velocidades:

- 🔬 **Agente Investigador** — Se ejecuta cada 30 minutos, realizando brainstorming y buscando tropos literarios
- ✍️ **Agente Escritor** — Se ejecuta cada 2 horas, compilando la investigación en un nuevo capítulo

## 🏗️ Arquitectura

El sistema se divide en tres capas:

```
┌─────────────────────────────────────────────────────┐
│              CAPA COGNITIVA (APIs de IA)             │
│   Cualquier API OpenAI-compatible (configurable)    │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│          CAPA DE EJECUCIÓN (GitHub Actions)          │
│   cron_researcher.yml (*/30 min)                    │
│   cron_writer.yml     (cada 2 horas)                   │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│        CAPA DE ALMACENAMIENTO (Repositorio)         │
│   Biblia │ Config │ Research Log │ Capítulos        │
└─────────────────────────────────────────────────────┘
```

## 📂 Estructura del Proyecto

```
AI-Novel-Studio/
├── .github/workflows/
│   ├── cron_researcher.yml     # Agente investigador (cada 30 min)
│   └── cron_writer.yml         # Agente escritor (cada 2 horas)
├── src/
│   ├── researcher.py           # Lógica del Agente Investigador
│   ├── writer.py               # Lógica del Agente Escritor
│   └── utils.py                # Funciones compartidas (API, Git)
├── data/
│   ├── config.json             # Panel de control de parámetros
│   ├── biblia.md               # Fichas de personajes, reglas, lore
│   ├── resúmenes.md            # Resumen condensado de la historia
│   └── research_log.txt        # Investigaciones acumuladas
├── chapters/                   # Directorio de salida de la novela
│   └── cap_001.md              # Capítulo piloto
├── requirements.txt            # Dependencias de Python
└── README.md                   # Este archivo
```

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/AI-Novel-Studio.git
cd AI-Novel-Studio
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la API Key

Configura tu API Key como variable de entorno:

```bash
export AI_API_KEY="tu-clave-secreta"
```

En GitHub: **Settings → Secrets and variables → Actions → New repository secret** → `AI_API_KEY`

> **Nota:** El sistema soporta cualquier proveedor OpenAI-compatible (Minimax, OpenAI, DeepSeek, Groq, Mistral, OpenRouter, Ollama local, etc.). Configura el endpoint y modelo en `data/config.json`.

### 4. Dar permisos de escritura al bot

En GitHub: **Settings → Actions → General → Workflow permissions** → Seleccionar **Read and write permissions** → Save

### 5. Personalizar la historia

Edita `data/config.json` para definir:
- Título de la novela
- Géneros y pesos (Rom-Com, Acción, Sci-Fi, etc.)
- Instrucciones de investigación y estilo de escritura

## 🎮 Panel de Control

El archivo `data/config.json` permite controlar la dirección de la historia **sin tocar código**:

| Parámetro | Descripción |
|-----------|-------------|
| `current_research_focus` | Dirige las investigaciones del agente |
| `genre_weights` | Balance entre géneros (Rom-Com, Acción, etc.) |
| `writing_style_override` | Instrucciones de estilo para el escritor |
| `target_chapter_words` | Longitud objetivo por capítulo |
| `temperature_*` | Creatividad de la IA (0.0 = conservador, 1.0 = creativo) |

## 📚 ¿Cómo leer la novela?

- Navega a la carpeta `chapters/` del repositorio
- Los capítulos se publican en formato Markdown (`.md`)
- cada 2 horas se genera un nuevo capítulo automáticamente

## 📖 Documentación

| Documento | Descripción |
|-----------|-------------|
| [SPEC.md](SPEC.md) | Requisitos funcionales del sistema |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Diseño interno del sistema |
| [PLANNING.md](PLANNING.md) | Tareas actuales y progreso |
| [ROADMAP.md](ROADMAP.md) | Dirección a largo plazo |
| [AGENTS.md](AGENTS.md) | Instrucciones para agentes IA |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guía de contribución |

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

> *A.I. Novel Studio — Donde la Inteligencia Artificial escribe las historias del mañana, hoy.*

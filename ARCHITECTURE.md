# ARCHITECTURE.md — Arquitectura del Sistema A.I. Novel Studio

> **Versión:** 1.1.0  
> **Última actualización:** 2026-04-11

---

## 1. Vista de Alto Nivel

A.I. Novel Studio utiliza una arquitectura de tres capas sin servidor (serverless), orquestada mediante GitHub Actions:

```
┌───────────────────────────────────────────────────────────────────┐
│                    CAPA COGNITIVA (APIs de IA)                     │
│                                                                   │
│   ┌─────────────────┐                ┌─────────────────────┐     │
│   │  Proveedor IA   │                │  Proveedores        │     │
│   │  (Configurable) │                │  Alternativos       │     │
│   └────────┬────────┘                └─────────────────────┘     │
└────────────┼──────────────────────────────────────────────────────┘
             │ HTTPS (Bearer Token)
┌────────────▼──────────────────────────────────────────────────────┐
│                 CAPA DE EJECUCIÓN (GitHub Actions)                │
│                                                                   │
│   ┌─────────────────────┐      ┌───────────────────────────┐     │
│   │  cron_researcher    │      │  cron_writer              │     │
│   │  (cada 2 horas)     │      │  (cada 4 horas)            │     │
│   │                     │      │                           │     │
│   │  → researcher.py    │      │  → writer.py              │     │
│   │  → utils.py         │      │  → utils.py               │     │
│   └─────────┬───────────┘      └────────────┬──────────────┘     │
└─────────────┼───────────────────────────────┼────────────────────┘
              │ git commit + push             │ git commit + push
┌─────────────▼───────────────────────────────▼────────────────────┐
│              CAPA DE ALMACENAMIENTO (Repositorio GitHub)          │
│                                                                   │
│   data/config.json          ← Panel de control                        │
│   data/biblia.md            ← Reglas del mundo y personajes           │
│   data/canon.md             ← Hechos inamovibles de la historia       │
│   data/personajes.json      ← Memoria de largo plazo de personajes    │
│   data/cronología.json      ← Memoria temporal de eventos             │
│   data/hilos_narrativos.json← Subtramas activas                       │
│   data/semillas.json        ← Foreshadowing plantado y pendiente      │
│   data/resúmenes.md         ← Historia condensada                     │
│   data/research_log.txt     ← Buffer de investigación                 │
│   chapters/cap_XXX.md       ← Salida: capítulos publicados            │
└───────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes del Sistema

### 2.1 `src/utils.py` — Módulo de Utilidades

**Responsabilidad:** Funciones compartidas entre agentes.

| Función | Descripción |
|---------|-------------|
| `load_config()` | Lee `data/config.json` y devuelve el dict de configuración |
| `save_config(data)` | Escribe actualizaciones en `data/config.json` |
| `call_ai_api(prompt, system_prompt, temperature, max_tokens)` | Realiza llamadas HTTP al modelo de IA |

**Dependencias:** `os`, `json`, `requests`

### 2.2 `src/researcher.py` — Agente Investigador

**Responsabilidad:** Generar ideas, tropos y material de investigación.

**Flujo:**
1. Leer configuración (`load_config()`)
2. Extraer foco de investigación y pesos de género
3. Construir prompt de investigación
4. Llamar a la API de IA
5. Append del resultado a `data/research_log.txt`

**Trigger:** `cron_researcher.yml` cada 2 horas.

### 2.3 `src/writer.py` — Agente Escritor

**Responsabilidad:** Compilar toda la información y redactar un capítulo.

**Flujo:**
1. Leer configuración, biblia, resúmenes y log de investigación
2. Construir mega-prompt con todo el contexto
3. Llamar a la API de IA con el mega-prompt
4. Guardar capítulo como `chapters/cap_XXX.md`
5. Actualizar `last_chapter_number` en config
6. Vaciar `data/research_log.txt`

**Trigger:** `cron_writer.yml` cada 4 horas.

---

## 3. Flujo de Datos

```
┌──────────────┐    ┌────────────────┐    ┌───────────────────┐
│ config.json  │───▶│ researcher.py  │───▶│ research_log.txt  │
│ (parámetros) │    │ (cada 2 horas) │    │ (append mode)     │
└──────────────┘    └────────────────┘    └────────┬──────────┘
                                                   │
┌──────────────┐    ┌────────────────┐             │
│ biblia.md    │───▶│                │◄────────────┘
│ resúmenes.md │───▶│  writer.py     │
│ config.json  │───▶│  (cada 4 horas)   │
└──────────────┘    └───────┬────────┘
                            │
                    ┌───────▼────────┐    ┌──────────────────┐
                    │ cap_XXX.md     │    │ research_log.txt │
                    │ (nuevo cap)    │    │ (vaciado)        │
                    └────────────────┘    └──────────────────┘
                            │
                    ┌───────▼────────┐
                    │ config.json    │
                    │ (chapter++)    │
                    └────────────────┘
```

---

## 4. Relaciones de Dependencia

```
researcher.py ──imports──▶ utils.py
writer.py     ──imports──▶ utils.py
utils.py      ──imports──▶ os, json, requests (stdlib + pip)

cron_researcher.yml ──runs──▶ researcher.py
cron_writer.yml     ──runs──▶ writer.py
```

---

## 5. Decisiones de Arquitectura Clave

### ADR-001: GitHub Actions como Orquestador

**Contexto:** Se necesita ejecución periódica sin servidor dedicado.  
**Decisión:** Usar GitHub Actions con cron schedules.  
**Consecuencias:** Coste cero en repositorios públicos. Limitación de ~2000 minutos/mes en repos privados.

### ADR-002: Repositorio como Base de Datos

**Contexto:** Se necesita persistencia de estado entre ejecuciones.  
**Decisión:** Usar archivos del repositorio (JSON, Markdown, TXT) como almacenamiento.  
**Consecuencias:** Simplicidad extrema. Sin dependencias de bases de datos. Historial via Git. Limitación de concurrencia (posibles conflictos de merge en ejecuciones simultáneas).

### ADR-003: Dos Velocidades de Ejecución

**Contexto:** Se quiere maximizar la calidad de la IA sin saturar su ventana de contexto ni exceder timeouts de GitHub Actions.  
**Decisión:** Investigador cada 2 horas (2 iteraciones) + Escritor cada 4 horas.  
**Consecuencias:** El investigador genera ideas focalizadas sin saturar contexto. El escritor tiene ~2 informes de investigación por ciclo, suficiente para contexto rico sin sobrecarga. Timeout de GitHub Actions aumentado a 120 min para el escritor.

### ADR-004: API Compatible con OpenAI

**Contexto:** El modelo principal puede cambiar en cualquier momento.  
**Decisión:** Usar formato de payload compatible con API tipo OpenAI. El endpoint, modelo y API Key se leen de `config.json`.  
**Consecuencias:** Cambiar de proveedor requiere solo modificar `api_host`, `model_name` y `api_key_env` en config. Soporta Minimax, OpenAI, DeepSeek, Groq, Mistral, OpenRouter, Ollama local, y cualquier otro compatible.

---

## 6. Tecnologías

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Lenguaje | Python | 3.10+ |
| HTTP Client | requests | última estable |
| Orquestador | GitHub Actions | v3/v4 |
| IA Model | Configurable (OpenAI-compatible) | API Chat |
| Formato | Markdown (.md) | — |
| Config | JSON | — |

---

## 7. Limitaciones Conocidas

1. **Concurrencia:** Si el investigador y escritor se ejecutan simultáneamente, puede haber conflictos de git. Mitigado con `git pull --rebase` antes del push en ambos workflows.
2. **Contexto limitado:** El tamaño del mega-prompt está limitado por la ventana de contexto del modelo. Reducido `researcher_calls_per_run` a 2 para evitar saturación.
3. **Timeout de GitHub Actions:** El escritor tiene timeout de 120 minutos para acomodar modelos lentos como MiniMax-M2.7.
3. **Rate limiting:** APIs gratuitas pueden tener límites de solicitudes por minuto.
4. **Drift narrativo:** Sin supervisión humana, la historia puede derivar temáticamente.

# SPEC.md — Especificación del Sistema A.I. Novel Studio

> **Versión:** 1.1.0  
> **Última actualización:** 2026-04-11  
> **Estado:** En Producción — 12 capítulos generados

---

## 1. Descripción General

A.I. Novel Studio es un sistema de generación automatizada de literatura (Novelas Ligeras) que opera de forma autónoma mediante GitHub Actions, utilizando modelos de IA (LLMs) para investigar, planificar y redactar capítulos de forma continua.

---

## 2. Requisitos Funcionales

### RF-01: Ejecución Autónoma

- El sistema DEBE ejecutarse sin intervención humana una vez configurado.
- El sistema DEBE utilizar GitHub Actions como motor de orquestación.
- El sistema DEBE soportar ejecución manual vía `workflow_dispatch`.

### RF-02: Agente Investigador

- El agente investigador DEBE ejecutarse cada 2 horas (cron: `0 */2 * * *`).
- DEBE leer la configuración dinámica desde `data/config.json`.
- DEBE generar ideas basadas en los pesos de género configurados.
- DEBE añadir resultados en modo append a `data/research_log.txt`.
- DEBE hacer commit y push automático de los cambios.

### RF-03: Agente Escritor

- El agente escritor DEBE ejecutarse cada 4 horas (cron: `0 */4 * * *`).
- DEBE leer la Biblia de la novela (`data/biblia.md`).
- DEBE leer los resúmenes acumulados (`data/resúmenes.md`).
- DEBE consumir el log de investigación completo (`data/research_log.txt`).
- DEBE generar un capítulo en formato Markdown con el patrón `cap_XXX.md`.
- DEBE actualizar el número de capítulo en `data/config.json`.
- DEBE vaciar `data/research_log.txt` tras la escritura.
- DEBE hacer commit y push de todos los archivos modificados.

### RF-04: Panel de Control

- La configuración DEBE leerse desde `data/config.json` en cada ejecución.
- El archivo DEBE permitir cambiar en caliente:
  - Proveedor y modelo de IA
  - Tokens máximos y temperaturas
  - Título y arco narrativo actual
  - Pesos de géneros literarios
  - Foco de investigación
  - Estilo de escritura

### RF-05: Continuidad Narrativa

- Cada capítulo DEBE mantener continuidad con los anteriores.
- El sistema DEBE inyectar la Biblia, resúmenes y notas de investigación al escritor.
- El escritor DEBE respetar las reglas del mundo definidas en la Biblia.

---

## 3. Requisitos No Funcionales

### RNF-01: Seguridad

- Las API Keys NUNCA deben estar en el código fuente.
- Las API Keys DEBEN gestionarse exclusivamente mediante GitHub Secrets.
- El repositorio NO debe contener credenciales en texto plano.

### RNF-02: Coste

- El sistema DEBE operar con APIs gratuitas o de bajo coste (cualquier proveedor OpenAI-compatible).
- El coste de cómputo DEBE ser cero (GitHub Actions en repositorios públicos).

### RNF-03: Fiabilidad

- Los workflows DEBEN ser idempotentes: si no hay cambios, no se genera commit.
- Los scripts DEBEN manejar errores de API de forma graceful (sin crashear el workflow).

### RNF-04: Rendimiento

- Cada ejecución del investigador DEBE completarse en menos de 5 minutos.
- Cada ejecución del escritor DEBE completarse en menos de 10 minutos.

---

## 4. Contratos de API

### API de IA (OpenAI-compatible — Configurable)

El sistema soporta **cualquier proveedor** con formato OpenAI-compatible. El endpoint, modelo y API Key se configuran en `data/config.json`.

**Proveedores probados:** Minimax, OpenAI, DeepSeek, Groq, Mistral, OpenRouter, Ollama (local).

**Endpoint:** Configurable via `system_settings.api_host`  
**Ejemplo:** `https://api.minimax.io/v1/chat/completions`

**Headers:**
```
Authorization: Bearer {AI_API_KEY}
Content-Type: application/json
```

**Payload:**
```json
{
  "model": "<configurable via model_name>",
  "messages": [
    {"role": "system", "content": "<system_prompt>"},
    {"role": "user", "content": "<user_prompt>"}
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**Respuesta esperada:**
```json
{
  "choices": [
    {
      "message": {
        "content": "<texto_generado>"
      }
    }
  ]
}
```

---

## 5. Estructuras de Datos

### `data/config.json`

```json
{
  "system_settings": {
    "api_provider": "string",
    "model_name": "string",
    "max_tokens_output": "integer (500-8000)",
    "temperature_research": "float (0.0-1.0)",
    "temperature_writing": "float (0.0-1.0)"
  },
  "story_status": {
    "title": "string",
    "current_arc": "string",
    "target_chapter_words": "integer (500-5000)",
    "last_chapter_number": "integer (>= 0)"
  },
  "genre_weights": {
    "_comment": "Catálogo completo de 150+ géneros. Solo los que tienen peso > 0 se usan.",
    "rom_com": "integer (0-100)",
    "action": "integer (0-100)",
    "sci_fi": "integer (0-100)",
    "mystery": "integer (0-100)",
    "slice_of_life": "integer (0-100)",
    "isekai": "integer (0-100)",
    "cultivation": "integer (0-100)",
    "litrpg": "integer (0-100)",
    "...150+ géneros disponibles": "ver data/config.json para la lista completa"
  },
  "dynamic_instructions": {
    "current_research_focus": "string",
    "writing_style_override": "string"
  }
}
```

### Formato de Capítulo (`chapters/cap_XXX.md`)

```markdown
# Capítulo {número}

{contenido_del_capítulo}
```

### Formato de Research Log (`data/research_log.txt`)

```
--- INFORME DE INVESTIGACIÓN ---
{contenido_de_ideas_generadas}

--- INFORME DE INVESTIGACIÓN ---
{más_ideas_acumuladas}
```

---

## 6. Fuera de Alcance (v1.0)

El sistema **NO** hará lo siguiente en la versión 1.0:

- ❌ Interfaz web o GUI para lectura
- ❌ Generación de ilustraciones o imágenes
- ❌ Traducción automática a otros idiomas
- ❌ Interacción con lectores (comentarios, votaciones)
- ❌ Múltiples novelas simultáneas en un solo repositorio
- ❌ Edición colaborativa humano-IA en tiempo real
- ❌ Publicación en plataformas externas (Wattpad, RoyalRoad, etc.)

---

## 7. Reglas de Negocio

1. Los pesos de género en `genre_weights` DEBEN sumar 100.
2. El campo `last_chapter_number` se incrementa automáticamente tras cada capítulo.
3. El `research_log.txt` se vacía tras cada ejecución del escritor.
4. Los capítulos se nombran con padding de 3 dígitos: `cap_001.md`, `cap_002.md`, etc.
5. Si la API falla, el workflow debe terminar sin generar archivos corruptos.

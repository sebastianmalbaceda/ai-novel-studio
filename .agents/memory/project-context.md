# Contexto del Proyecto — A.I. Novel Studio

> **Última actualización:** 2026-04-06  
> **Versión:** 1.0.0

## Descripción

A.I. Novel Studio es un sistema autónomo de generación de novelas ligeras
que utiliza GitHub Actions como orquestador y APIs de IA (Minimax) como
motor cognitivo.

## Estado Actual

- **Fase:** MVP v1.0 completado
- **Capítulos generados:** 1 (piloto)
- **Agentes activos:** Investigador (15 min) + Escritor (1h)
- **API provider:** Minimax v1

## Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `src/utils.py` | Funciones compartidas (API, config) |
| `src/researcher.py` | Agente investigador |
| `src/writer.py` | Agente escritor |
| `data/config.json` | Panel de control dinámico |
| `data/biblia.md` | Reglas del mundo y personajes |
| `data/resúmenes.md` | Historia condensada |

## Decisiones Tomadas

1. GitHub Actions como orquestador (coste cero)
2. Repositorio como base de datos (simplicidad)
3. Dos velocidades: investigación rápida + escritura pausada
4. API compatible OpenAI para portabilidad

## Próximas Prioridades

1. Reintentos con exponential backoff
2. Tests unitarios
3. Validación de config.json
4. Logging estructurado

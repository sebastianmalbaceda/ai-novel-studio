# PLANNING.md — Tareas de Implementación

> **Última actualización:** 2026-04-06  
> **Sprint actual:** v1.0 — MVP

---

## Estado del Proyecto

| Fase | Estado |
|------|--------|
| Documentación del proyecto | ✅ Completada |
| Scaffolding de directorios | ✅ Completada |
| Scripts de Python (src/) | ✅ Completada |
| GitHub Actions (workflows) | ✅ Completada |
| Datos iniciales (data/) | ✅ Completada |
| Capítulo piloto | ✅ Completada |

---

## Tareas Completadas

- [x] Crear `README.md` con descripción del proyecto y quick start
- [x] Crear `SPEC.md` con requisitos funcionales y no funcionales
- [x] Crear `ARCHITECTURE.md` con diseño de tres capas
- [x] Crear `ROADMAP.md` con visión a largo plazo
- [x] Crear `PLANNING.md` (este archivo)
- [x] Crear `AGENTS.md` con instrucciones para agentes IA
- [x] Crear `CONTRIBUTING.md` con guía de contribución
- [x] Crear `CHANGELOG.md` con historial de versiones
- [x] Crear `SECURITY.md` con política de seguridad
- [x] Crear `CODE_OF_CONDUCT.md` con código de conducta
- [x] Crear `LICENSE` (MIT)
- [x] Crear `PROMPTS.md` con templates de prompts
- [x] Crear `AI_WORKFLOW.md` con pipeline de desarrollo
- [x] Crear `.gitignore`
- [x] Crear `.agentignore`
- [x] Crear `.env.example`
- [x] Crear `requirements.txt`
- [x] Crear `src/utils.py` con funciones compartidas
- [x] Crear `src/researcher.py` con agente investigador
- [x] Crear `src/writer.py` con agente escritor
- [x] Crear `data/config.json` con panel de control
- [x] Crear `data/biblia.md` con mundo y personajes
- [x] Crear `data/resúmenes.md` con resumen inicial
- [x] Crear `data/research_log.txt` vacío
- [x] Crear `chapters/cap_001.md` capítulo piloto
- [x] Crear `.github/workflows/cron_researcher.yml`
- [x] Crear `.github/workflows/cron_writer.yml`
- [x] Crear `.agents/config.json`
- [x] Crear `.agents/mcp.json`
- [x] Crear `.agents/skills/` con skills iniciales
- [x] Crear `.agents/rules/` con reglas por contexto
- [x] Crear `.agents/prompts/` con prompts reutilizables
- [x] Crear `.agents/memory/project-context.md`
- [x] Crear `docs/` con documentación extendida

---

## Próximas Tareas (v1.1)

- [ ] Implementar reintentos con backoff exponencial en `utils.py`
- [ ] Añadir validación de `config.json` con schema
- [ ] Crear tests unitarios para `utils.py`
- [ ] Crear tests unitarios para `researcher.py`
- [ ] Crear tests unitarios para `writer.py`
- [ ] Implementar logging estructurado
- [ ] Auto-generación de resúmenes post-escritura

---

## Bloqueantes

Ninguno actualmente.

---

## Decisiones Pendientes

1. ~~¿Usar Minimax o cambiar a modelo gratuito alternativo?~~ ✅ Resuelto: Sistema model-agnostic, soporta cualquier proveedor.
2. ¿Implementar un agente editor en v1.1 o esperar a v1.5?
3. ¿Frecuencia óptima del investigador: 15 min o 20 min?

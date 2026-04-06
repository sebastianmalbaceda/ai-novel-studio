# Changelog

Todos los cambios notables en este proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Planificado
- Reintentos con exponential backoff en llamadas a API
- Validación de schema para `config.json`
- Tests unitarios para todos los módulos
- Logging estructurado con timestamps

---

## [1.0.0] — 2026-04-06

### Añadido
- Estructura completa del repositorio
- Agente Investigador (`src/researcher.py`) — ejecución cada 15 minutos
- Agente Escritor (`src/writer.py`) — ejecución cada hora
- Utilidades compartidas (`src/utils.py`) — llamadas API, configuración
- Panel de control dinámico (`data/config.json`)
- Biblia de la novela con mundo, personajes y reglas (`data/biblia.md`)
- Sistema de resúmenes acumulativos (`data/resúmenes.md`)
- Buffer de investigación (`data/research_log.txt`)
- GitHub Actions: workflow del investigador (`cron_researcher.yml`)
- GitHub Actions: workflow del escritor (`cron_writer.yml`)
- Capítulo piloto de demostración (`chapters/cap_001.md`)
- Documentación completa del proyecto (README, SPEC, ARCHITECTURE, etc.)
- Configuración de agentes IA (AGENTS.md, .agents/, skills)
- Pipeline de desarrollo IA (AI_WORKFLOW.md)

### Seguridad
- API Keys gestionadas exclusivamente via GitHub Secrets
- `.gitignore` configurado para excluir archivos sensibles
- `.agentignore` para proteger credenciales de agentes IA

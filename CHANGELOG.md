# Changelog

Todos los cambios notables en este proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Planificado
- Tests unitarios para todos los módulos
- Logging estructurado con timestamps
- Soporte para múltiples proveedores de IA simultáneos

---

## [1.1.0] — 2026-04-11

### Corregido
- **CRÍTICO:** Función duplicada `update_memory_with_ai` en `writer.py` — la segunda definición (validación de idioma) sobreescribía la primera (actualización de memoria). Renombrada a `validate_chapter_language`.
- Variable `content` no definida en validación de idioma — corregida a `chapter_content`.
- Función `validate_chapter_language` no existía pero se llamaba en el flujo principal.
- La memoria profunda (personajes, cronología, hilos, semillas, canon) nunca se actualizaba — ahora parsea JSON de la IA y actualiza archivos correctamente.

### Optimizado
- `researcher_calls_per_run` reducido de 5 a 2 — evita saturación de ventana de contexto.
- `max_tokens_output` reducido de 3000 a 2500 — mejora tiempos de respuesta y reduce timeouts.
- Frecuencia del investigador: cada 30 min → cada 2 horas.
- Frecuencia del escritor: cada 2 horas → cada 4 horas.
- Timeout del escritor en GitHub Actions: 60 min → 120 min.
- Timeout del investigador en GitHub Actions: 120 min → 30 min.
- Ambos workflows ahora hacen `git pull --rebase` antes del push para evitar conflictos.
- El workflow del escritor ahora incluye todos los archivos de memoria en el commit.

### Eliminado
- Capítulos 10-15 originales (redundantes e inconsistentes) — reemplazados por nuevos caps 10-12 consolidados.
- Los caps 9-13 originales repetían la misma escena matutina con revelaciones redundantes.

### Añadido
- Nuevo capítulo 9: "El Número Que No Debería Existir" — consolida la revelación de la frecuencia.
- Nuevo capítulo 10: "Lo Que Nunca Pudo Decir" — la madre como Integrada, video del contacto.
- Nuevo capítulo 11: "Límites de la Coherencia" — Haruto le cuenta todo a Kenji.
- Nuevo capítulo 12: "El Peso de las Respuestas Sin Dar" — Watcher_0 es IA, Sujeto M-07.
- Sistema de memoria profunda: `personajes.json`, `cronología.json`, `hilos_narrativos.json`, `semillas.json`, `canon.md` — todos actualizados y coherentes.

### Documentación
- README.md actualizado con nuevas frecuencias y archivos de memoria.
- SPEC.md actualizado a v1.1.0.
- ARCHITECTURE.md actualizado con diagramas y decisiones de arquitectura revisadas.
- CHANGELOG.md (este archivo) creado.

---

## [1.0.0] — 2026-04-06

### Añadido
- Estructura completa del repositorio
- Agente Investigador (`src/researcher.py`) — ejecución cada 30 minutos
- Agente Escritor (`src/writer.py`) — ejecución cada 2 horas
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

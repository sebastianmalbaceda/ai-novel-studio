# ROADMAP.md — Hoja de Ruta de A.I. Novel Studio

> **Última actualización:** 2026-04-06

---

## Visión a Largo Plazo

Convertir A.I. Novel Studio en la plataforma de referencia para generación autónoma de literatura, capaz de producir historias con calidad editorial mínima, personalización profunda y publicación multiplataforma.

---

## v1.0 — MVP: Generación Autónoma Básica ✅ (Actual)

**Objetivo:** Sistema funcional end-to-end que genera capítulos cada 2 horas.

- [x] Estructura de repositorio definida
- [x] Agente Investigador (`researcher.py`)
- [x] Agente Escritor (`writer.py`)
- [x] Utilidades compartidas (`utils.py`)
- [x] GitHub Actions: cron investigador (30 min)
- [x] GitHub Actions: cron escritor (2 horas)
- [x] Panel de control vía `config.json`
- [x] Biblia de la novela (mundo, personajes, reglas)
- [x] Sistema de resúmenes acumulativos
- [x] Documentación completa del proyecto

---

## v1.1 — Mejoras de Estabilidad

**Objetivo:** Hacer el sistema robusto ante fallos y mejorar la calidad narrativa.

- [ ] Manejo de errores de API con reintentos (retry con exponential backoff)
- [ ] Logging estructurado con timestamps
- [ ] Validación de `config.json` antes de cada ejecución
- [x] Resúmenes automáticos post-escritura (condensar capítulo para `resúmenes.md`)
- [x] Tests unitarios (cobertura inicial para `utils.py` y `researcher.py`)
- [ ] Detección de conflictos de git y resolución automática

---

## v1.5 — Calidad Narrativa

**Objetivo:** Mejorar la coherencia y profundidad de los capítulos generados.

- [ ] Agente Editor: revisión automática del capítulo antes de publicar
- [ ] Memoria a largo plazo: base de conocimiento de personajes activa
- [ ] Arcos narrativos con inicio/nudo/desenlace programáticos
- [ ] Generación de cliffhangers al final de cada capítulo
- [ ] Soporte para múltiples puntos de vista (POV)

---

## v2.0 — Multi-Modelo y Personalización

**Objetivo:** Soporte para múltiples proveedores de IA y personalización avanzada.

- [ ] Interfaz web (GitHub Pages) para leer la novela
- [ ] Soporte OpenAI, Anthropic, Gemini como proveedores alternativos
- [ ] Selección dinámica de modelo por tarea (investigación vs escritura)
- [ ] Sistema de votos: lectores pueden influir en la dirección de la trama
- [ ] Generación de portadas con IA generativa de imágenes

---

## v3.0 — Publicación y Distribución

**Objetivo:** Publicación automatizada en plataformas externas.

- [ ] Exportación a EPUB/PDF
- [ ] Publicación automática en Wattpad / Royal Road / Webnovel
- [ ] Sistema de newsletter con capítulos por email
- [ ] Traducción automática a inglés y japonés
- [ ] Múltiples novelas simultáneas en un solo repositorio

---

## Horizonte Futuro

- 🎨 Generación de ilustraciones por capítulo (manga panels)
- 🎵 Generación de banda sonora ambiental por escena
- 🎙️ Narración TTS (Text-to-Speech) de capítulos
- 🌐 Comunidad de lectores con sistema de comentarios
- 🤖 Agentes autónomos de feedback que simulan lectores

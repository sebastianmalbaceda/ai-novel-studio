# Guía de Contribución — A.I. Novel Studio

¡Gracias por tu interés en contribuir a A.I. Novel Studio! 🎉

## 📋 Antes de Empezar

1. Lee el [README.md](README.md) para entender el proyecto
2. Revisa [ARCHITECTURE.md](ARCHITECTURE.md) para entender la estructura
3. Consulta [PLANNING.md](PLANNING.md) para ver las tareas pendientes
4. Lee [SPEC.md](SPEC.md) para entender los requisitos

## 🔀 Flujo de Trabajo Git

### Ramas

- `main` — Rama de producción. Solo se actualiza via PR o GitHub Actions.
- `feature/<descripción>` — Para nuevas funcionalidades.
- `fix/<descripción>` — Para corrección de bugs.
- `docs/<descripción>` — Para cambios en documentación.

### Formato de Commits

Utilizamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: añadir agente editor para revisión automática
fix: corregir encoding en research_log.txt
docs: actualizar README con instrucciones de deploy
chore: actualizar requirements.txt
refactor: extraer lógica de prompts a módulo separado
```

### Proceso de Pull Request

1. Haz fork del repositorio
2. Crea una rama descriptiva: `git checkout -b feature/agente-editor`
3. Realiza tus cambios siguiendo las convenciones del proyecto
4. Asegúrate de que los scripts funcionan: `python src/researcher.py` (con mock)
5. Haz commit con formato convencional
6. Abre un Pull Request con descripción detallada

## 🎨 Convenciones de Código

### Python

- **Versión:** Python 3.10+
- **Estilo:** PEP 8 con líneas de máximo 100 caracteres
- **Docstrings:** Google style
- **Encoding:** UTF-8 en todos los archivos
- **Imports:** stdlib → terceros → locales, separados por línea en blanco

```python
# ✅ Correcto
import os
import json

import requests

from utils import load_config, call_ai_api
```

### Archivos de Datos

- **JSON:** Indentación de 4 espacios, `ensure_ascii=False`
- **Markdown:** Encabezados con `#`, listas con `-`, código con triple backtick
- **TXT:** UTF-8, saltos de línea Unix (LF)

### YAML (Workflows)

- Indentación de 2 espacios
- Nombres descriptivos en español para los steps
- Comentarios explicativos en secciones complejas

## 🧪 Testing

Antes de enviar un PR, verifica:

```bash
# Verificar sintaxis Python
python -m py_compile src/utils.py
python -m py_compile src/researcher.py
python -m py_compile src/writer.py

# Ejecutar tests (cuando existan)
python -m pytest tests/
```

## 📝 Documentación

- Toda nueva funcionalidad DEBE documentarse
- Actualiza `CHANGELOG.md` con tus cambios
- Si modificas la arquitectura, actualiza `ARCHITECTURE.md`
- Si añades tareas, actualiza `PLANNING.md`

## ⚠️ Lo Que NO Hacer

- ❌ **NUNCA** incluir API Keys o secretos en el código
- ❌ **NUNCA** modificar `data/config.json` con datos reales de producción
- ❌ **NUNCA** hacer push directamente a `main` (solo las GitHub Actions)
- ❌ **NUNCA** borrar capítulos existentes en `chapters/`
- ❌ **NUNCA** modificar workflows sin aprobación previa

## 💬 ¿Preguntas?

Abre un [Issue](https://github.com/tu-usuario/AI-Novel-Studio/issues) con la etiqueta `question`.

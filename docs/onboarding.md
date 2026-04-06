# Onboarding — A.I. Novel Studio

> Guía para nuevos desarrolladores que se incorporan al proyecto.

## 🎯 ¿Qué hace este proyecto?

A.I. Novel Studio genera novelas ligeras de forma autónoma usando IA. El sistema funciona con dos agentes:

1. **Investigador** — Cada 15 minutos investiga tropos, ideas y giros argumentales.
2. **Escritor** — Cada hora compila la investigación y escribe un capítulo.

Todo se ejecuta en GitHub Actions. No hay servidor.

## 📁 Archivos que debes leer primero

1. `README.md` — Vista general
2. `ARCHITECTURE.md` — Cómo funciona internamente
3. `SPEC.md` — Qué debe hacer exactamente
4. `AGENTS.md` — Si eres un agente IA, empieza aquí
5. `data/config.json` — El "panel de control" de la historia

## 🛠️ Setup en 5 minutos

```bash
git clone https://github.com/tu-usuario/AI-Novel-Studio.git
cd AI-Novel-Studio
pip install -r requirements.txt
export AI_API_KEY="tu-key"
cd src && python researcher.py
```

## 📂 Dónde está cada cosa

| Necesito... | Miro en... |
|-------------|-----------|
| Cambiar la historia | `data/config.json` |
| Entender los personajes | `data/biblia.md` |
| Ver capítulos generados | `chapters/` |
| Modificar la lógica de investigación | `src/researcher.py` |
| Modificar la lógica de escritura | `src/writer.py` |
| Cambiar la conexión a la API | `src/utils.py` |
| Ajustar la automatización | `.github/workflows/` |

## ⚠️ Reglas que no puedes romper

1. **NUNCA** commitear API Keys
2. **NUNCA** borrar capítulos existentes
3. **NUNCA** hardcodear valores que están en `config.json`
4. **SIEMPRE** usar `utils.call_ai_api()` para llamar a la IA
5. **SIEMPRE** encoding UTF-8 en todo

## 🤝 Siguiente paso

Revisa `PLANNING.md` para ver las tareas pendientes y elige una.

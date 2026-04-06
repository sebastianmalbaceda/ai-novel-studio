---
name: generate-chapter-summary
description: |
  Genera un resumen conciso de un capítulo recién escrito y lo añade
  a data/resúmenes.md. Activar después de que el agente escritor
  genere un nuevo capítulo. No activar para capítulos ya resumidos.
---

# Instrucciones: Generación de Resumen de Capítulo

## Cuándo Usar

Después de que `writer.py` genere un nuevo capítulo en `chapters/cap_XXX.md`.

## Proceso

1. Leer el capítulo recién generado desde `chapters/cap_XXX.md`
2. Generar un resumen de máximo 200 palabras que capture:
   - Eventos principales
   - Desarrollo de personajes relevante
   - Revelaciones o giros de trama
   - Estado de las relaciones al final del capítulo
3. Añadir el resumen a `data/resúmenes.md` en formato append

## Formato de Salida

```markdown
### Capítulo {número}

{resumen_del_capítulo}

---
```

## Reglas

- NUNCA modificar resúmenes de capítulos anteriores
- El resumen debe ser suficiente para dar contexto al escritor sin leer el capítulo completo
- Mantener encoding UTF-8
- Usar append mode al escribir en `resúmenes.md`

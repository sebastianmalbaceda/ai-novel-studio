---
name: code-review
description: |
  Realiza una revisión estructurada del código Python del proyecto.
  Activar cuando se solicite revisión de código, antes de merges,
  o cuando se detecten cambios significativos en los scripts principales.
  No activar para cambios de documentación o configuración.
---

# Instrucciones: Revisión de Código

## Checklist de Revisión

Seguir estas categorías en orden:

### 1. Seguridad
- [ ] No hay API Keys, tokens o secretos hardcodeados
- [ ] Las variables de entorno se leen con `os.environ.get()`
- [ ] No hay inyección de código en prompts construidos dinámicamente
- [ ] Los archivos sensibles están en `.gitignore` y `.agentignore`

### 2. Correctitud
- [ ] La lógica cumple con lo definido en `SPEC.md`
- [ ] Los archivos se abren con `encoding='utf-8'`
- [ ] Las rutas son relativas desde `src/` (e.g., `../data/config.json`)
- [ ] El manejo de errores es adecuado (no raw exceptions)
- [ ] Los archivos JSON se escriben con `ensure_ascii=False`

### 3. Arquitectura
- [ ] Sigue el diseño definido en `ARCHITECTURE.md`
- [ ] Todas las llamadas a API pasan por `utils.call_ai_api()`
- [ ] Los parámetros dinámicos se leen de `config.json` (no hardcodeados)
- [ ] No hay dependencias circulares entre módulos

### 4. Estilo
- [ ] Código legible y bien estructurado
- [ ] Docstrings presentes en funciones públicas
- [ ] Variables con nombres descriptivos en inglés
- [ ] Imports organizados: stdlib → third-party → local

### 5. Performance
- [ ] No hay operaciones de I/O innecesarias
- [ ] Los archivos se cierran correctamente (usar `with`)
- [ ] No hay loops que podrían ser problemáticos con archivos grandes

## Formato de Feedback

```
## Resumen
[Breve descripción de los hallazgos]

## Issues Críticos
- 🔴 [Problema que DEBE corregirse]

## Sugerencias
- 🟡 [Mejora recomendada]

## Lo Positivo
- 🟢 [Algo bien hecho que vale la pena destacar]
```

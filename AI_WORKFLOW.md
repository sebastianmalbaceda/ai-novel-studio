# AI_WORKFLOW.md — Pipeline de Desarrollo IA

> **Última actualización:** 2026-04-06  
> Define cómo los modelos de IA colaboran en el ciclo de desarrollo del proyecto.

---

## Pipeline de Desarrollo

```
PLAN → BUILD → REVIEW → TEST → ITERATE
```

---

## Fase PLAN

**Modelo recomendado:** Claude Opus 4.6 (o equivalente de alta capacidad de razonamiento)

**Responsabilidades:**

- Analizar requisitos desde `SPEC.md`
- Diseñar el plan de implementación detallado
- Actualizar `PLANNING.md` con tareas específicas y accionables
- Validar el plan contra `ARCHITECTURE.md`
- Identificar ambigüedades y marcarlas antes de empezar a codificar
- Estimar complejidad y secuenciación de tareas

**Output:** Un `PLANNING.md` actualizado con tareas claras e inequívocas que un agente builder pueda ejecutar sin tomar decisiones de diseño.

---

## Fase BUILD

**Modelo recomendado:** Claude Sonnet 4.6 (estándar para codificación agéntica)  
**Alternativa de bajo coste:** GLM-5 (open weights, MIT, ~20-25% del coste de Sonnet)

**Patrón de optimización de costes:**
> Usar Sonnet para archivos complejos y lógica core; GLM-5 (o similar) para tareas de implementación rutinarias y bien especificadas.

**Responsabilidades:**

- Implementar tareas listadas en `PLANNING.md` una a una
- Seguir convenciones de codificación de `AGENTS.md`
- Seguir el diseño de `SPEC.md` y `ARCHITECTURE.md`
- Cargar skills relevantes (`SKILL.md`) según necesidad
- NO tomar decisiones arquitectónicas — escalar al planner
- Marcar tareas como completadas en `PLANNING.md`

---

## Fase REVIEW

**Modelo recomendado:** Claude Opus 4.6 (mismo nivel que el planner)

**Responsabilidades:**

- Auditar todo el código nuevo producido en la fase build
- Detectar bugs, edge cases y errores de lógica
- Verificar cumplimiento con `ARCHITECTURE.md` y `SPEC.md`
- Verificar seguridad: inyección, exposición de secretos, auth, validación de input
- Sugerir mejoras con cambios propuestos específicos
- Verificar que `PLANNING.md` refleja lo que se construyó

---

## Fase TEST

**Modelo:** Cualquier modelo capaz de codificación (clase Sonnet o equivalente)

**Responsabilidades:**

- Generar tests unitarios, de integración y edge-case
- Validar comportamiento descrito en `SPEC.md`
- Ejecutar suite de tests existente y reportar fallos
- Identificar paths de código sin testear
- Documentar gaps de cobertura

---

## Fase ITERATE

Después de review y testing:

- Corregir todos los issues detectados (la fase build maneja las correcciones)
- Re-ejecutar tests para confirmar que los issues están resueltos
- Actualizar `PLANNING.md` (marcar completados, añadir nuevas tareas del review)
- Actualizar `CHANGELOG.md` con cambios notables
- Continuar al siguiente ciclo de desarrollo

---

## Checkpoints de Supervisión Humana

Los humanos son responsables de:

- ✅ Aprobar cambios arquitectónicos antes de implementación
- ✅ Revisar y mergear pull requests
- ✅ Validar que el comportamiento enviado coincide con la intención del usuario
- ✅ Actualizar `SPEC.md` cuando cambian los requisitos
- ✅ Auditar `PLANNING.md` periódicamente para detectar drift

**Puntos de integración recomendados:**

1. Output del planner (`PLANNING.md` diff) revisado antes de empezar build
2. Output del build (pull request) revisado antes de merge
3. Cambios sensibles de seguridad siempre requieren sign-off humano

---

## Asignación de Modelos para Este Proyecto

| Fase | Modelo Principal | Alternativa |
|------|-----------------|-------------|
| PLAN | Claude Opus 4.6 | — |
| BUILD | Claude Sonnet 4.6 | GLM-5 (rutinas) |
| REVIEW | Claude Opus 4.6 | — |
| TEST | Claude Sonnet 4.6 | GLM-5 |
| ITERATE | Claude Sonnet 4.6 | GLM-5 |

# PROMPTS.md — Templates de Prompts Reutilizables

> **Última actualización:** 2026-04-06  
> Prompts estandarizados para tareas recurrentes del proyecto.

---

## 1. Prompt de Investigación (Agente Investigador)

```
Eres un investigador experto en tropos literarios, ciencia ficción y manga.

Realiza una investigación y lluvia de ideas sobre el siguiente tema:
"{research_focus}"

Busca formas originales de integrar estos elementos en una historia que combina:
- Rom-Com ({rom_com}% de peso)
- Acción ({action}% de peso)  
- Sci-Fi ({sci_fi}% de peso)

Genera 3 ideas concretas (eventos, revelaciones de misterio o interacciones entre personajes).
Devuelve solo el texto de tus ideas, estructurado en puntos.
```

---

## 2. Prompt de Escritura (Agente Escritor)

```
Eres un aclamado autor de novelas ligeras especializadas en mezclar Rom-com, Acción y Sci-Fi.

Vas a escribir el CAPÍTULO {chapter_num} de la novela "{title}".

[REGLAS DEL MUNDO Y PERSONAJES (BIBLIA)]
{biblia_content}

[RESUMEN DE LA HISTORIA HASTA AHORA]
{summary_content}

[NOTAS DE INVESTIGACIÓN]
{research_notes}

[INSTRUCCIONES DE ESTILO]
{style_override}
El capítulo debe tener aproximadamente {target_words} palabras.

Escribe directamente el capítulo en formato Markdown.
```

---

## 3. Prompt de Revisión de Código

```
Revisa el siguiente código Python del proyecto A.I. Novel Studio.

Criterios de revisión:
1. ¿El código maneja errores de API correctamente?
2. ¿Los archivos se abren con encoding UTF-8?
3. ¿Las rutas son relativas desde src/?
4. ¿Se usa config.json para valores dinámicos (sin hardcoding)?
5. ¿Hay riesgos de seguridad (API keys expuestas)?

Código a revisar:
{code_content}
```

---

## 4. Prompt de Generación de Tests

```
Genera tests unitarios (pytest) para el siguiente módulo Python:

Módulo: {module_name}
Código:
{code_content}

Requisitos:
- Usar pytest y unittest.mock para mockear llamadas a API
- Cubrir casos happy path y error handling
- Verificar que los archivos se leen/escriben correctamente
- No hacer llamadas reales a APIs externas
```

---

## 5. Prompt de Resumen de Capítulo

```
Lee el siguiente capítulo de una novela ligera y genera un resumen conciso (máximo 200 palabras) que capture:

1. Eventos principales que ocurren
2. Desarrollo de personajes relevante
3. Revelaciones o giros de trama
4. Estado de las relaciones entre personajes al final del capítulo

Capítulo:
{chapter_content}
```

---

## 6. Prompt de Generación de PR Description

```
Genera una descripción de Pull Request para los siguientes cambios:

Archivos modificados:
{changed_files}

Resumen de cambios:
{change_summary}

Formato de salida:
## Descripción
[Explicación breve]

## Cambios
- [Lista de cambios principales]

## Testing
- [Cómo se verificaron los cambios]

## Checklist
- [ ] Código revisado
- [ ] Tests actualizados
- [ ] Documentación actualizada
```

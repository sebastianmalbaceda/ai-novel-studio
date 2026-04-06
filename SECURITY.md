# Política de Seguridad — A.I. Novel Studio

## Versiones Soportadas

| Versión | Soportada |
|---------|-----------|
| 1.0.x   | ✅ Sí      |
| < 1.0   | ❌ No      |

## Reportar una Vulnerabilidad

Si descubres una vulnerabilidad de seguridad en A.I. Novel Studio, por favor repórtala de forma responsable.

### Cómo Reportar

1. **NO** abras un Issue público para vulnerabilidades de seguridad.
2. Envía un email a: **[security@ai-novel-studio.dev]** (o abre un Security Advisory privado en GitHub).
3. Incluye:
   - Descripción de la vulnerabilidad
   - Pasos para reproducirla
   - Impacto potencial
   - Sugerencia de corrección (si la tienes)

### Qué Esperar

- **Confirmación:** Recibirás una respuesta en un plazo de 48 horas.
- **Evaluación:** Se evaluará la gravedad en un plazo de 5 días laborables.
- **Resolución:** Se publicará un parche y un aviso de seguridad una vez corregido.

## Prácticas de Seguridad del Proyecto

### API Keys y Secretos

- Las API Keys **NUNCA** se incluyen en el código fuente.
- Todas las credenciales se gestionan mediante **GitHub Secrets**.
- El archivo `.env` está excluido via `.gitignore`.
- Los agentes IA tienen restricciones via `.agentignore`.

### GitHub Actions

- Los workflows solo tienen permisos de **read+write** sobre el repositorio propio.
- No se utilizan tokens de terceros sin cifrado.
- Las Actions usan versiones fijadas de las acciones oficiales (pinned versions).

### Datos Generados

- Los capítulos generados son contenido de ficción sin datos personales.
- El `research_log.txt` se vacía periódicamente.
- No se recopilan datos de usuarios.

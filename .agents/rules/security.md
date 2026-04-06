# Reglas de Seguridad — A.I. Novel Studio

## Secretos y Credenciales

- NUNCA incluir API Keys en código fuente
- NUNCA hacer commit de archivos `.env` con valores reales
- SIEMPRE usar GitHub Secrets para credenciales en workflows
- SIEMPRE usar `os.environ.get()` para leer secrets
- Si una API Key aparece en un diff, RECHAZAR el cambio inmediatamente

## GitHub Actions

- Usar versiones pinneadas de Actions (e.g., `actions/checkout@v3`)
- No exponer secrets en logs (no usar `echo $VARIABLE`)
- Workflow permissions: solo `read-write` sobre el repositorio propio
- No utilizar tokens de acceso personal (PAT) en workflows

## Archivos Sensibles

Verificar que estos archivos están en `.gitignore`:
- `.env`, `.env.local`, `.env.production`
- `*.key`, `*.pem`, `*.p12`
- `venv/`, `.venv/`

Verificar que estos archivos están en `.agentignore`:
- `.env`
- `.git/`
- `*.key`, `*.pem`

## Input Validation

- Los prompts construidos dinámicamente deben sanitizar inputs
- `config.json` debe validarse antes de inyectarse en prompts
- No confiar en el contenido de `research_log.txt` como código ejecutable

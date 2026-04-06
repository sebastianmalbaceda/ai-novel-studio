# Deployment — A.I. Novel Studio

## Entorno de Ejecución

A.I. Novel Studio se despliega exclusivamente en **GitHub Actions**. No requiere servidor dedicado, hosting, ni infraestructura propia.

## Requisitos de Deploy

1. Repositorio en GitHub (público para Actions gratuitos)
2. API Key de tu proveedor de IA configurada como GitHub Secret
3. Permisos de escritura habilitados para GitHub Actions

## Proceso de Deploy

### 1. Push a GitHub

```bash
git add .
git commit -m "feat: deploy inicial de AI Novel Studio"
git push origin main
```

### 2. Configurar Secrets

Navegar a: **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Descripción |
|-------------|-------------|
| `AI_API_KEY` | API Key del proveedor de IA (nombre configurable en config.json) |

### 3. Habilitar Workflow Permissions

Navegar a: **Settings → Actions → General → Workflow permissions**  
Seleccionar: **Read and write permissions**

### 4. Verificar Workflows

Los workflows se activarán automáticamente según sus schedules cron:
- **Investigador:** cada 30 minutos
- **Escritor:** cada 2 horas

### Ejecución Manual

Ambos workflows tienen `workflow_dispatch` habilitado:
1. Ir a **Actions** en el repositorio
2. Seleccionar el workflow deseado
3. Clic en **Run workflow**

## Monitorización

- Los logs de cada ejecución se encuentran en **Actions → [Workflow] → [Run]**
- Los commits automáticos aparecen con el autor `github-actions[bot]`
- Si un workflow falla, GitHub envía notificación por email

## Limitaciones

- **Repos públicos:** Actions ilimitados y gratuitos
- **Repos privados:** ~2000 minutos/mes en plan gratuito
- **Scheduling:** GitHub puede retrasar ejecuciones cron en períodos de alta carga

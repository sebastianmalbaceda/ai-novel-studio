# ADR-001: GitHub Actions como Orquestador

**Estado:** Aceptado  
**Fecha:** 2026-04-06  
**Decisores:** Equipo fundador

## Contexto

El sistema necesita ejecutar scripts de Python de forma periódica (cada 15 minutos y cada hora) sin mantener un servidor dedicado encendido 24/7. Se evaluaron las siguientes opciones:

1. **Servidor VPS** (DigitalOcean, AWS EC2)
2. **Serverless Functions** (AWS Lambda, Google Cloud Functions)
3. **GitHub Actions con cron schedules**
4. **Cron local** en un ordenador personal

## Decisión

Usar **GitHub Actions** con schedules cron como motor de orquestación.

## Consecuencias

### Positivas
- **Coste cero** en repositorios públicos (Actions ilimitados)
- **Sin mantenimiento** de infraestructura
- **Integración nativa** con el repositorio (checkout, commit, push)
- **Logs automáticos** y notificaciones de fallo
- **Manual dispatch** disponible para ejecuciones bajo demanda

### Negativas
- **Precisión del cron:** GitHub puede retrasar ejecuciones hasta 15 minutos en picos de carga
- **Límite en repos privados:** ~2000 minutos/mes en plan gratuito
- **Sin estado persistente:** Las VMs son efímeras, todo el estado debe vivir en el repo
- **Concurrencia limitada:** Posibles conflictos de git si dos workflows se ejecutan simultáneamente

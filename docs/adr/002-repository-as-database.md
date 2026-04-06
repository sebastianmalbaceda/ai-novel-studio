# ADR-002: Repositorio como Base de Datos

**Estado:** Aceptado  
**Fecha:** 2026-04-06  
**Decisores:** Equipo fundador

## Contexto

El sistema necesita persistir estado entre ejecuciones: configuración, contenido narrativo (Biblia, resúmenes), investigación acumulada, y los capítulos generados. Se evaluaron:

1. **Base de datos relacional** (PostgreSQL, SQLite)
2. **Base de datos NoSQL** (MongoDB, Firebase)
3. **Archivos en el repositorio** (JSON, Markdown, TXT)
4. **Almacenamiento en la nube** (S3, GCS)

## Decisión

Usar **archivos dentro del repositorio** (JSON para config, Markdown para contenido, TXT para logs) como sistema de persistencia.

## Consecuencias

### Positivas
- **Simplicidad extrema:** No hay infraestructura externa
- **Historial completo:** Git proporciona versionado automático de todos los cambios
- **Portabilidad:** Todo el proyecto es un directorio de archivos
- **Legibilidad:** Cualquiera puede leer los datos directamente en GitHub
- **Coste cero:** Sin servicios de base de datos que pagar

### Negativas
- **No es concurrent-safe:** Escrituras simultáneas pueden causar conflictos de merge
- **Sin queries:** No se pueden hacer consultas complejas sobre los datos
- **Límite de tamaño:** Repositorios de GitHub tienen límite recomendado de 1GB
- **Sin transacciones:** No hay atomicidad en escrituras multi-archivo
- **Performance:** Git no está optimizado para escrituras frecuentes de alta velocidad

## Mitigaciones

- El scheduling de workflows minimiza conflictos (escritor en minuto 0, investigador en 15/30/45)
- Los archivos son pequeños (KB, no MB)
- El `research_log.txt` se vacía cada hora, controlando el crecimiento

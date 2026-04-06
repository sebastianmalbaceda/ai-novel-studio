# Build & Run — A.I. Novel Studio

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git
- Cuenta de GitHub con acceso a Actions

## Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/AI-Novel-Studio.git
cd AI-Novel-Studio

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución Manual

```bash
# Configurar API Key (el nombre de la variable se define en config.json → api_key_env)
export AI_API_KEY="tu-clave-secreta"

# Ejecutar el investigador
cd src
python researcher.py

# Ejecutar el escritor
python writer.py
```

## Verificación de Sintaxis

```bash
python -m py_compile src/utils.py
python -m py_compile src/researcher.py
python -m py_compile src/writer.py
```

## Tests

```bash
python -m pytest tests/ -v
```

## Configuración de GitHub Actions

1. **Secrets:** Settings → Secrets → New: `AI_API_KEY` (o el nombre definido en `api_key_env`)
2. **Permisos:** Settings → Actions → General → Workflow permissions → Read and write
3. Los workflows se activarán automáticamente tras push a main.

# Manual de Despliegue: API REST con FastAPI y Frontend con Angular

Este manual describe los pasos y requisitos necesarios para configurar y ejecutar tanto el backend (API REST con FastAPI) como el frontend (con Angular) de este proyecto.

---

## 1. Backend (API con FastAPI y Python)

Esta sección cubre la configuración del servidor y la base de datos.

### 1.1. Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.7+**: Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- **MySQL**: La API está configurada para usar MySQL. Necesitas un servidor de MySQL en ejecución. Puedes usar XAMPP, WAMP, MAMP o una instalación nativa.

### 1.2. Creación de un Entorno Virtual

Es una buena práctica aislar las dependencias de tu proyecto en un entorno virtual.

**1. Crear el entorno virtual:**
Navega a la raíz del proyecto (`API-REST`) y ejecuta:
```bash
python -m venv venv
```
Esto creará una carpeta `venv` que contendrá las librerías de Python para este proyecto.

**2. Activar el entorno virtual:**

- **En Windows (cmd.exe):**
  ```bash
  .\venv\Scripts\activate
  ```
- **En macOS y Linux (bash/zsh):**
  ```bash
  source venv/bin/activate
  ```
Sabrás que el entorno está activo porque el nombre del entorno `(venv)` aparecerá al inicio de la línea de comandos.

### 1.3. Instalación de Dependencias

Con el entorno virtual activado, instala todas las librerías necesarias.

**1. Crea un archivo `requirements.txt`** en la raíz del proyecto con el siguiente contenido:
```
fastapi
uvicorn[standard]
mysql-connector-python
pydantic
```

**2. Instala las dependencias** ejecutando:
```bash
pip install -r requirements.txt
```

### 1.4. Configuración de la Base de Datos

La API necesita conectarse a una base de datos MySQL.

1.  **Crea una base de datos** en tu servidor MySQL. Puedes llamarla `user` o como prefieras.
2.  **Actualiza los datos de conexión** en el archivo `main.py`, dentro del diccionario `DB_CONFIG`:
    ```python
    DB_CONFIG = {
        "host": "localhost",      # O la IP de tu servidor de BD
        "user": "root",           # Tu usuario de MySQL
        "password": "tu_contraseña", # Tu contraseña de MySQL
        "database": "user"        # El nombre de la base de datos que creaste
    }
    ```

### 1.5. Ejecutar la API

Una vez que todo está configurado, puedes iniciar el servidor de la API.

```bash
uvicorn main:app --reload
```

- `main`: Se refiere al archivo `main.py`.
- `app`: Se refiere al objeto `app = FastAPI()` dentro de `main.py`.
- `--reload`: Hace que el servidor se reinicie automáticamente cada vez que detecta un cambio en el código.

La API estará disponible en `http://127.0.0.1:8000`. Puedes ver la documentación interactiva en `http://127.0.0.1:8000/docs`.

---

## 2. Frontend (Angular)

Esta sección cubre la configuración del cliente web que consumirá la API.

### 2.1. Prerrequisitos

- **Node.js y npm**: Angular requiere Node.js. Descárgalo desde [nodejs.org](https://nodejs.org/). `npm` (Node Package Manager) se instala automáticamente con Node.js.

### 2.2. Instalación de Angular CLI

La **Angular CLI** es una herramienta de línea de comandos que te ayuda a crear y gestionar proyectos de Angular.

Para instalarla de forma global en tu sistema, abre una terminal y ejecuta:
```bash
npm install -g @angular/cli
```
- `-g`: Flag para indicar que la instalación es global.

### 2.3. Comandos Básicos de Angular CLI

Aquí tienes los comandos más comunes para trabajar con un proyecto de Angular.

**1. Crear un nuevo proyecto:**
```bash
ng new nombre-del-proyecto
```
La CLI te hará algunas preguntas (si quieres añadir routing, qué formato de estilos prefieres, etc.).

**2. Levantar el servidor de desarrollo:**
Navega dentro de la carpeta de tu nuevo proyecto y ejecuta:
```bash
ng serve -o
```
- `ng serve`: Compila la aplicación y la sirve en un servidor local.
- `-o` (o `--open`): Abre automáticamente tu navegador en `http://localhost:4200/`.

**3. Generar Componentes:**
Los componentes son los bloques de construcción principales de una aplicación de Angular.
```bash
ng generate component nombre-del-componente
# Abreviatura:
ng g c nombre-del-componente
```

**4. Generar Servicios:**
Los servicios son ideales para la lógica que no está atada a una vista específica, como hacer peticiones HTTP a tu API.
```bash
ng generate service nombre-del-servicio
# Abreviatura:
ng g s nombre-del-servicio
```

**5. Generar Módulos:**
Los módulos ayudan a organizar la aplicación en bloques de funcionalidad cohesivos.
```bash
ng generate module nombre-del-modulo
# Abreviatura:
ng g m nombre-del-modulo
```

**6. Construir la aplicación para producción:**
Cuando tu aplicación está lista para ser desplegada, necesitas compilarla para producción.
```bash
ng build --configuration production
```
Este comando creará una carpeta `dist/nombre-del-proyecto/` con todos los archivos estáticos (HTML, CSS, JS) optimizados que puedes desplegar en un servidor web.

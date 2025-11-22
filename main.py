# main.py
# Importa las clases y funciones necesarias de FastAPI, Pydantic y otras bibliotecas.
# FastAPI: El framework para construir APIs.
# HTTPException: Para manejar errores HTTP.
# Depends: Para la inyección de dependencias (no se usa directamente aquí, pero es común en FastAPI).
# CORSMiddleware: Para permitir solicitudes de diferentes orígenes (Cross-Origin Resource Sharing).
# BaseModel, Field, ConfigDict: De Pydantic, para la validación y configuración de modelos de datos.
# Optional, List: De typing, para definir tipos de datos.
# mysql.connector: El conector oficial de Python para MySQL.
# Error: Clase de excepción de mysql.connector.
# asynccontextmanager: Para gestionar recursos de forma asíncrona (en este caso, la base de datos).
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
import mysql.connector
from mysql.connector import Error
from contextlib import asynccontextmanager

# Define un diccionario con los parámetros de conexión a la base de datos MySQL.
DB_CONFIG = {
    "host": "localhost",  # La dirección del servidor de la base de datos.
    "user": "root",       # El nombre de usuario para la conexión.
    "password": "dariozayas",   # La contraseña del usuario.
    "database": "user"    # El nombre de la base de datos a la que se conectará.
}

# Define una función para obtener una conexión a la base de datos.
def get_db_connection():
    try:
        # Intenta establecer una conexión usando la configuración definida en DB_CONFIG.
        conn = mysql.connector.connect(**DB_CONFIG)
        # Devuelve el objeto de conexión si tiene éxito.
        return conn
    except Error as e:
        # Si ocurre un error de conexión, lanza una excepción HTTP 500 con un mensaje de error.
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {str(e)}")

# Define un modelo Pydantic base para un usuario.
class UsuarioBase(BaseModel):
    """
    Modelo base con los campos comunes de un usuario.
    """
    # Define el campo 'name' como una cadena de texto, obligatorio, con longitud entre 1 y 100.
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    # Define el campo 'description' como una cadena de texto, obligatorio, con longitud entre 1 y 100.
    description: str = Field(..., min_length=1, max_length=100, description="Descripción del usuario")

    # Configuración del modelo Pydantic.
    model_config = ConfigDict(
        from_attributes=True,  # Permite que el modelo se cree a partir de atributos de objeto (ORM).
        json_schema_extra={  # Define un ejemplo para la documentación de la API.
            "example": {
                "name": "Juan Pérez",
                "description": "juan@example.com",
            }
        }
    )

# Define un modelo para la creación de un usuario, que hereda de UsuarioBase.
class UsuarioCreate(UsuarioBase):
    """Modelo para crear un usuario"""
    # No añade campos adicionales, utiliza los de la clase base.
    pass

# Define un modelo para la actualización de un usuario.
class UsuarioUpdate(BaseModel):
    """
    Modelo para actualizar un usuario (todos los campos son opcionales).
    """
    # Define el campo 'name' como opcional (puede ser None).
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    # Define el campo 'description' como opcional (puede ser None).
    description: Optional[str] = Field(None, min_length=1, max_length=100)

# Define el modelo completo de un usuario, incluyendo el ID.
class Usuario(UsuarioBase):
    """
    Modelo completo de usuario incluyendo ID.
    """
    # Define el campo 'id' como un entero obligatorio.
    id: int = Field(..., description="ID único del usuario")

    # Configuración del modelo Pydantic.
    model_config = ConfigDict(
        from_attributes=True,  # Permite la creación desde atributos de objeto.
        json_schema_extra={  # Define un ejemplo para la documentación.
            "user": {
                "name": "Juan Pérez",
                "description": "juan@example.com"
            }
        }
    )

# Define un gestor de ciclo de vida asíncrono para la aplicación FastAPI.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación (startup).
    try:
        # Obtiene una conexión a la base de datos.
        connection = get_db_connection()
        # Crea un cursor para ejecutar comandos SQL.
        cursor = connection.cursor()
        # Ejecuta una consulta SQL para crear la tabla 'user' si no existe.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200),
                description VARCHAR(400),
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
        """)
        # Confirma los cambios en la base de datos.
        connection.commit()
        # Cierra el cursor.
        cursor.close()
        # Cierra la conexión.
        connection.close()
        # Imprime un mensaje de éxito en la consola.
        print("Base de datos inicializada correctamente")
    except Exception as e:
        # Si ocurre un error, imprime un mensaje de error.
        print("Error al inicializar base de datos:", e)

    # La aplicación se ejecuta después de este 'yield'.
    yield

    # Código que se ejecuta al apagar la aplicación (shutdown).
    print("Cerrando aplicación...")

# Crea una instancia de la aplicación FastAPI.
app = FastAPI(
    title="API CRUD de Usuarios",  # Título de la API.
    description="API REST para gestionar usuarios con operaciones CRUD completas",  # Descripción.
    version="1.0.0",  # Versión de la API.
    lifespan=lifespan  # Asigna el gestor de ciclo de vida.
)

# Añade el middleware de CORS a la aplicación.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de cualquier origen.
    allow_credentials=True,  # Permite el envío de credenciales (cookies, etc.).
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.).
    allow_headers=["*"],  # Permite todas las cabeceras HTTP.
)

# Define un endpoint para la ruta raíz de la API.
@app.get("/", tags=["Root"])
async def root():
    # Devuelve un mensaje JSON de bienvenida.
    return {"mensaje": "API CRUD de Usuarios funcionando correctamente"}

# Define un endpoint para crear un nuevo usuario (método POST).
@app.post("/usuarios/", response_model=Usuario, status_code=201, tags=["Usuarios"])
async def crear_usuario(usuario: UsuarioCreate):
    try:
        # Obtiene una conexión a la base de datos.
        connection = get_db_connection()
        # Crea un cursor.
        cursor = connection.cursor()

        # Define la consulta SQL para insertar un nuevo usuario.
        query = "INSERT INTO user (name, description) VALUES (%s, %s)"
        # Define los valores a insertar, tomados del modelo de entrada.
        values = (usuario.name, usuario.description)

        # Ejecuta la consulta con los valores.
        cursor.execute(query, values)
        # Confirma la transacción.
        connection.commit()

        # Obtiene el ID del último registro insertado.
        usuario_id = cursor.lastrowid
        # Cierra el cursor.
        cursor.close()
        # Cierra la conexión.
        connection.close()

        # Devuelve el nuevo usuario creado, incluyendo su ID.
        return Usuario(id=usuario_id, **usuario.dict())

    except mysql.connector.IntegrityError:
        # Si ocurre un error de integridad (ej. 'description' duplicado), lanza un error 400.
        raise HTTPException(status_code=400, detail="El description ya está registrado")
    except Error as e:
        # Para otros errores de base de datos, lanza un error 500.
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

# Define un endpoint para obtener todos los usuarios (método GET).
@app.get("/usuarios/", response_model=List[Usuario], tags=["Usuarios"])
async def obtener_usuarios():
    try:
        # Obtiene una conexión a la base de datos.
        connection = get_db_connection()
        # Crea un cursor que devuelve filas como diccionarios.
        cursor = connection.cursor(dictionary=True)

        # Ejecuta la consulta para seleccionar todos los usuarios.
        cursor.execute("SELECT * FROM user")
        # Obtiene todos los resultados.
        usuarios = cursor.fetchall()

        # Cierra el cursor.
        cursor.close()
        # Cierra la conexión.
        connection.close()

        # Devuelve la lista de usuarios.
        return usuarios

    except Error as e:
        # Si hay un error, lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

# Define un endpoint para obtener un usuario por su ID (método GET).
@app.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
async def obtener_usuario(usuario_id: int):
    try:
        # Obtiene una conexión a la base de datos.
        connection = get_db_connection()
        # Crea un cursor que devuelve filas como diccionarios.
        cursor = connection.cursor(dictionary=True)

        # Ejecuta la consulta para seleccionar un usuario por su ID.
        cursor.execute("SELECT * FROM user WHERE id = %s", (usuario_id,))
        # Obtiene un solo resultado.
        usuario = cursor.fetchone()

        # Cierra el cursor.
        cursor.close()
        # Cierra la conexión.
        connection.close()

        # Si no se encuentra el usuario, lanza un error 404.
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Devuelve el usuario encontrado.
        return usuario

    except Error as e:
        # Si hay un error, lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

# Define un endpoint para actualizar un usuario por su ID (método PUT).
@app.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
async def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate):
    try:
        # Obtiene una conexión a la base de datos.
        connection = get_db_connection()
        # Crea un cursor que devuelve filas como diccionarios.
        cursor = connection.cursor(dictionary=True)

        # Listas para construir la consulta de actualización dinámicamente.
        campos = []
        valores = []

        # Si se proporciona un nuevo nombre, lo añade a la consulta.
        if usuario.name is not None:
            campos.append("name = %s")
            valores.append(usuario.name)
        # Si se proporciona una nueva descripción, la añade a la consulta.
        if usuario.description is not None:
            campos.append("description = %s")
            valores.append(usuario.description)

        # Si no se proporcionó ningún campo para actualizar, lanza un error 400.
        if not campos:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        # Añade el ID del usuario al final de la lista de valores.
        valores.append(usuario_id)

        # Construye la consulta SQL de actualización.
        query = f"UPDATE user SET {', '.join(campos)} WHERE id = %s"
        # Ejecuta la consulta.
        cursor.execute(query, valores)
        # Confirma la transacción.
        connection.commit()

        # Si ninguna fila fue afectada, significa que el usuario no fue encontrado.
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Vuelve a consultar la base de datos para obtener el usuario actualizado.
        cursor.execute("SELECT * FROM user WHERE id = %s", (usuario_id,))
        usuario_actualizado = cursor.fetchone()

        # Cierra el cursor.
        cursor.close()
        # Cierra la conexión.
        connection.close()

        # Devuelve el usuario actualizado.
        return usuario_actualizado

    except mysql.connector.IntegrityError:
        # Si hay un error de integridad, lanza un error 400.
        raise HTTPException(status_code=400, detail="El description ya está registrado")
    except Error as e:
        # Para otros errores, lanza un error 500.
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

# Define un endpoint para eliminar un usuario por su ID (método DELETE).
@app.delete("/usuarios/{usuario_id}", status_code=204, tags=["Usuarios"])
async def eliminar_usuario(usuario_id: int):
    try:
        # Obtiene una conexión a la base de datos.
        connection = get_db_connection()
        # Crea un cursor.
        cursor = connection.cursor()

        # Ejecuta la consulta para eliminar el usuario.
        cursor.execute("DELETE FROM user WHERE id = %s", (usuario_id,))
        # Confirma la transacción.
        connection.commit()

        # Si ninguna fila fue afectada, el usuario no fue encontrado.
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Cierra el cursor.
        cursor.close()
        # Cierra la conexión.
        connection.close()

        # Devuelve una respuesta sin contenido (código 204).
        return None

    except Error as e:
        # Si hay un error, lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

# Comentario para indicar cómo ejecutar la aplicación con uvicorn.
# uvicorn: El servidor ASGI.
# main: El nombre del archivo Python (main.py).
# app: El objeto FastAPI dentro del archivo.
# --reload: Hace que el servidor se reinicie automáticamente al detectar cambios en el código.
# Ejecutar: uvicorn main:app --reload
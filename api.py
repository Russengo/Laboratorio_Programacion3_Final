from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import sqlite3
import jwt

app = FastAPI()
security = HTTPBearer()


# Clave para JWT
SECRET_KEY = "programacion_laboratorio3"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30 

class Usuario:
    def __init__(self, usuario: str, contraseña: str):
        self.usuario = usuario
        self.contraseña = hashlib.md5(contraseña.encode()).hexdigest()

    @staticmethod
    def autenticar(usuario, contraseña):
        return usuario == "User" and contraseña == "1234"  

    def verificar_contraseña(self, contraseña):
        return hashlib.md5(contraseña.encode()).hexdigest() == self.contraseña

    def verificar_contraseña(self, contraseña):
        return hashlib.md5(contraseña.encode()).hexdigest() == self.contraseña
    
def generar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


class Tarea(BaseModel):
    titulo: str
    descripcion: str


#---------------Inicio conexiòn y creaciòn DB---------------#

class AdminTarea:
    def __init__(self):
        self.db_connection = sqlite3.connect('tareas.db')
        self.db_cursor = self.db_connection.cursor()
        self._crear_tabla_tareas()

    def _crear_tabla_tareas(self):
        query = """
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            estado TEXT,
            creada TEXT,
            actualizada TEXT
        )
        """
        self.db_cursor.execute(query)
        self.db_connection.commit()


    def agregar_tarea(self, titulo: str, descripcion: str):
        creada = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        actualizada = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        query = """
        INSERT INTO tareas (titulo, descripcion, estado, creada, actualizada)
        VALUES (?, ?, ?, ?, ?)
        """
        self.db_cursor.execute(query, (titulo, descripcion, 'pendiente', creada, actualizada))
        self.db_connection.commit()
        return self.db_cursor.lastrowid

    def eliminar_tarea(self, tarea_id: int):
        query = """
        DELETE FROM tareas WHERE id = ?
        """
        self.db_cursor.execute(query, (tarea_id,))
        self.db_connection.commit()
        return self.db_cursor.rowcount > 0

    def obtener_tareas(self):
        query = """
        SELECT * FROM tareas
        """
        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def actualizar_tarea(self, tarea_id: int, titulo: str, descripcion: str):
        actualizada = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        query = """
        UPDATE tareas SET titulo = ?, descripcion = ?, actualizada = ? WHERE id = ?
        """
        self.db_cursor.execute(query, (titulo, descripcion, actualizada, tarea_id))
        self.db_connection.commit()
        return self.db_cursor.rowcount > 0
    
#---------------Fin conexiòn DB---------------#

admin_tarea = AdminTarea()

class Credenciales(BaseModel):
    usuario: str
    contraseña: str


#---------------Inicio rutas FastApi---------------#

@app.post("/login")
async def login(credenciales: Credenciales):
    if Usuario.autenticar(credenciales.usuario, credenciales.contraseña):
        token = generar_token({"sub": credenciales.usuario})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")


@app.post("/tareas", dependencies=[Depends(verificar_token)])
async def crear_tarea(tarea: Tarea):
    tarea_id = admin_tarea.agregar_tarea(tarea.titulo, tarea.descripcion)
    return {"tarea_id": tarea_id}

@app.get("/tareas",  dependencies=[Depends(verificar_token)])
async def obtener_tareas():
    tareas = admin_tarea.obtener_tareas()
    return tareas

@app.put("/tareas/{tarea_id}",  dependencies=[Depends(verificar_token)])
async def actualizar_tarea(tarea_id: int, tarea: Tarea):
    if admin_tarea.actualizar_tarea(tarea_id, tarea.titulo, tarea.descripcion):
        return {"mensaje": "Tarea actualizada correctamente"}
    else:
        raise HTTPException(status_code=404, detail="No se pudo actualizar la tarea")

@app.delete("/tareas/{tarea_id}",  dependencies=[Depends(verificar_token)])
async def eliminar_tarea(tarea_id: int):
    if admin_tarea.eliminar_tarea(tarea_id):
        return {"mensaje": "Tarea eliminada correctamente"}
    else:
        raise HTTPException(status_code=404, detail="No se pudo eliminar la tarea")

#---------------Fin rutas FastApi---------------#

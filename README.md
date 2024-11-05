# Laboratorio3-Final

- **Alumno:** Russo, Matías.

## Descripción

Proyecto final para el laboratorio 3 conjunto con Programación 3. Este proyecto implementa un sistema de gestión de tareas utilizando FastAPI para el backend y Tkinter para la interfaz gráfica de usuario.

## Consigna

Crear una aplicación de servidor para administrar una lista de tareas. Utilizar FastAPI o similar para que responda al modelo Cliente/Servidor por medio del protocolo HTTP e implemente una API RESTful. Es indispensable que el servidor implemente JWT para autenticar y permitir la utilización de la API.

Para interactuar con el servidor se deberá desarrollar una GUI que permita consumir los recursos del servidor. La aplicación permitirá al usuario agregar, ver, actualizar y eliminar tareas. La contraseña del usuario debe estar encriptada con alguna función hash en la base de datos.

## Requisitos

- Utiliza SQLite para almacenar las tareas en una base de datos.
- Crea una clase `Tarea` que tenga las siguientes propiedades:

  - `id`
  - `titulo`
  - `descripcion`
  - `estado`
  - `creada`
  - `actualizada`

- Crea una clase `Administrador de Tareas (AdminTarea)` que maneje la interacción con la base de datos SQLite. La clase debe tener los siguientes métodos:
  - `agregar_tarea(tarea: Tarea) -> int`: Agrega una nueva tarea a la base de datos y devuelve su ID.
  - `traer_tarea(tarea_id: int) -> Tarea`: Obtiene una tarea de la base de datos según su ID y devuelve una instancia de la clase Tarea.
  - `actualizar_estado_tarea(tarea_id: int, estado: str)`: Actualiza el estado de una tarea en la base de datos según su ID.
  - `eliminar_tarea(tarea_id: int)`: Elimina una tarea de la base de datos según su ID.
  - `traer_todas_tareas() -> List[Tarea]`: Obtiene todas las tareas de la base de datos y devuelve una lista de instancias de la clase Tarea.

## Configuración

Para ejecutar la aplicación, sigue estos pasos:

1. **Instala las dependencias**:
   ```bash
   pip install requests fastapi pydantic uvicorn
   ```
2. Ejecuta en un primer terminal el servidor de la aplicación con uvicorn api:app --reload.
3. Ejecuta en una segunda terminal la interfaz gràfica con python grafica.py
4. USUARIO Y CONTRASEÑA ES: "User" - "1234"

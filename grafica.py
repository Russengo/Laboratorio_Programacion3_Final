import tkinter as tk
import tkinter.messagebox as messagebox
import requests

API_URL = "http://127.0.0.1:8000"
TOKEN = None

def iniciar_sesion():
    global TOKEN
    credenciales = {"usuario": "User", "contraseña": "1234"}
    response = requests.post(f"{API_URL}/login", json=credenciales)
    if response.status_code == 200:
        TOKEN = response.json()["access_token"]  # Guarda el token de acceso en la variable TOKEN
        texto_estado.config(text="Inicio de sesión exitoso", fg="green") #Actualiza el estado en caso de que el token sea correcto
        mostrar_gestion_tareas()
    else:
        texto_estado.config(text="Error en el inicio de sesión", fg="red")

def mostrar_gestion_tareas():
    frame_login.pack_forget()
    frame_gestion.pack(fill=tk.X)

def obtener_tareas():  # Verifica si el usuario iniciò sesiòn
    if not TOKEN:   
        texto_tareas.insert(tk.END, "Error: Debes iniciar sesión primero\n")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_URL}/tareas", headers=headers)
    if response.status_code == 200:
        tareas = response.json()
        texto_tareas.delete("1.0", tk.END)
        for tarea in tareas:
            texto_tareas.insert(tk.END, f"Tarea: {tarea[1]} - {tarea[2]} (ID: {tarea[0]})\n")
    else:
        texto_tareas.insert(tk.END, "Error al obtener tareas\n")

def crear_tarea(): # Verifica si el usuario iniciò sesiòn
    if not TOKEN:
        texto_estado.config(text="Error: Debes iniciar sesión primero", fg="red")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    titulo = entry_titulo.get()
    descripcion = entry_descripcion.get()

    if not titulo or not descripcion:
        messagebox.showwarning("Advertencia", "Los campos título y descripción son obligatorios.")
        return

    tarea = {"titulo": titulo, "descripcion": descripcion}
    response = requests.post(f"{API_URL}/tareas", json=tarea, headers=headers)

    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Tarea creada con éxito")
        entry_titulo.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        obtener_tareas()
    else:
        error_message = response.json().get("detail", "Error desconocido")
        messagebox.showerror("Error", f"Error al crear la tarea: {error_message}")

def actualizar_tarea(): # Verifica si el usuario iniciò sesiòn
    if not TOKEN:
        texto_estado.config(text="Error: Debes iniciar sesión primero", fg="red")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    tarea_id = entry_id.get()
    titulo = entry_titulo.get()
    descripcion = entry_descripcion.get()

    if not tarea_id or not titulo or not descripcion:
        messagebox.showwarning("Advertencia", "Los campos ID, título y descripción son obligatorios.")
        return

    tarea = {"titulo": titulo, "descripcion": descripcion}
    response = requests.put(f"{API_URL}/tareas/{tarea_id}", json=tarea, headers=headers)

    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Tarea actualizada con éxito")
        obtener_tareas()
    else:
        error_message = response.json().get("detail", "Error desconocido")
        messagebox.showerror("Error", f"Error al actualizar tarea: {error_message}")

def eliminar_tarea(): # Verifica si el usuario iniciò sesiòn
    if not TOKEN:
        texto_estado.config(text="Error: Debes iniciar sesión primero", fg="red")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    tarea_id = entry_id.get()

    if not tarea_id:
        messagebox.showwarning("Advertencia", "El campo ID es obligatorio para eliminar la tarea.")
        return

    response = requests.delete(f"{API_URL}/tareas/{tarea_id}", headers=headers)

    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Tarea eliminada con éxito")
        obtener_tareas()
    else:
        error_message = response.json().get("detail", "Error desconocido")
        messagebox.showerror("Error", f"Error al eliminar tarea: {error_message}")

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Gestión de Tareas")
ventana.geometry("500x550")
ventana.configure(bg="#234157")

# Frame para el formulario de inicio de sesión
frame_login = tk.Frame(ventana, bg="#dfedf7", bd=2, relief=tk.GROOVE)
frame_login.pack(pady=10, padx=10, fill=tk.X)

tk.Label(frame_login, text="Iniciar Sesión", bg="#dfedf7", font=("Arial", 16)).pack(pady=5)

boton_login = tk.Button(frame_login, text="Iniciar Sesión", command=iniciar_sesion, width=20)
boton_login.pack(pady=10)

# Etiqueta de estado
texto_estado = tk.Label(frame_login, text="Estado: No has iniciado sesión", bg="#dfedf7")
texto_estado.pack(pady=5)

# Frame para la gestión de tareas
frame_gestion = tk.Frame(ventana, bg="#ffffff", bd=2, relief=tk.GROOVE)

tk.Label(frame_gestion, text="ID de la tarea", bg="#ffffff").pack(pady=5)
entry_id = tk.Entry(frame_gestion)
entry_id.pack(pady=5)

tk.Label(frame_gestion, text="Título de la tarea", bg="#ffffff").pack(pady=5)
entry_titulo = tk.Entry(frame_gestion)
entry_titulo.pack(pady=5)

tk.Label(frame_gestion, text="Descripción de la tarea", bg="#ffffff").pack(pady=5)
entry_descripcion = tk.Entry(frame_gestion)
entry_descripcion.pack(pady=5)

# Botones para gestionar tareas
boton_frame = tk.Frame(frame_gestion, bg="#ffffff")
boton_frame.pack(pady=10)

boton_crear = tk.Button(boton_frame, text="Crear Tarea", command=crear_tarea, width=15)
boton_crear.pack(side=tk.LEFT, padx=5)

boton_actualizar = tk.Button(boton_frame, text="Actualizar Tarea", command=actualizar_tarea, width=15)
boton_actualizar.pack(side=tk.LEFT, padx=5)

boton_eliminar = tk.Button(boton_frame, text="Eliminar Tarea", command=eliminar_tarea, width=15)
boton_eliminar.pack(side=tk.LEFT, padx=5)

boton_obtener = tk.Button(boton_frame, text="Obtener Tareas", command=obtener_tareas, width=15)
boton_obtener.pack(side=tk.LEFT, padx=5)

# Área de texto para mostrar tareas
texto_tareas = tk.Text(ventana, height=20, width=60, bg="#ffffff", wrap=tk.WORD)
texto_tareas.pack(pady=10)

ventana.mainloop()

import tkinter as tk
from tkinter import Label, Frame, Toplevel, Button, messagebox
from PIL import Image, ImageTk
from database.db_connection import conectar_db

global usuario_actual
usuario_actual = None

def cargar_foto_perfil(label_foto, usuario_actual):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT foto_perfil FROM usuarios WHERE nombre_usuario=%s"
    cursor.execute(query, (usuario_actual,))
    resultado = cursor.fetchone()
    
    if resultado and resultado[0]:  # Si hay una ruta de foto de perfil almacenada
        ruta_foto = resultado[0]
        try:
            imagen = Image.open(ruta_foto)
            imagen.thumbnail((150, 150))
            imagen_tk = ImageTk.PhotoImage(imagen)
            label_foto.config(image=imagen_tk)
            label_foto.image = imagen_tk  # Guardar referencia a la imagen
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la foto de perfil: {e}")
    else:
        cargar_foto_predeterminada(label_foto)  # Cargar foto predeterminada si no hay foto en la base de datos

    conn.close()

def cargar_foto_predeterminada(label_foto):
    try:
        imagen = Image.open("img/perfil1.png")
        imagen.thumbnail((150, 150))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_foto.config(image=imagen_tk)
        label_foto.image = imagen_tk  # Guardar referencia a la imagen
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la foto de perfil predeterminada: {e}")


def mostrar_perfil(usuario, ventana_menu, root):
    global usuario_actual  # Declarar usuario_actual como global antes de asignarle un valor
    usuario_actual = usuario  # Asignar el usuario actual globalmente
    
    ventana_perfil = Toplevel()
    ventana_perfil.title("Perfil de Usuario")
    ventana_perfil.geometry("260x250+1+45")
    ventana_perfil.configure(bg="ivory2")
    ventana_perfil.resizable(False, False)
    
    
     # Quitar botones de minimizar y maximizar
    ventana_perfil.attributes('-toolwindow', True) 
    
    #Label(ventana_perfil, text="Perfil de Usuario", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold")).pack(pady=20)
    
    frame_principal = Frame(ventana_perfil, bg="ivory2")
    frame_principal.pack(pady=10)

    # Perfil de usuario
    Label(frame_principal, text=f"{usuario_actual}", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 20, "bold")).pack(pady=5)
    
    label_foto = Label(frame_principal, bg="ivory2")
    label_foto.pack(pady=10)
    cargar_foto_perfil(label_foto, usuario_actual)

    # Hacer la ventana de perfil modal
    ventana_perfil.grab_set()
    ventana_perfil.focus_set()
    ventana_perfil.wait_window()

    ventana_perfil.mainloop()


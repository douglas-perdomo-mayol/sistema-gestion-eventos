import tkinter as tk
from tkinter import Label, Frame, Button, filedialog, messagebox, Toplevel, Entry
from PIL import Image, ImageTk
from database.db_connection import conectar_db

def actualizar_foto_perfil(ruta_foto, usuario_actual):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "UPDATE usuarios SET foto_perfil=%s WHERE nombre_usuario=%s"
    cursor.execute(query, (ruta_foto, usuario_actual))
    conn.commit()
    conn.close()

def cambiar_foto(label_foto, usuario_actual):
    ruta_foto = filedialog.askopenfilename(title="Seleccionar nueva foto de perfil", filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png")])
    if ruta_foto:
        try:
            imagen = Image.open(ruta_foto)
            imagen.thumbnail((150, 150))
            imagen_tk = ImageTk.PhotoImage(imagen)
            label_foto.config(image=imagen_tk)
            label_foto.image = imagen_tk  # Guardar referencia a la imagen
            actualizar_foto_perfil(ruta_foto, usuario_actual)  # Guardar la ruta en la base de datos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la foto de perfil: {e}")

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

def eliminar_cuenta(usuario_actual, ventana_configuracion, root, ventana_menu):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        # Eliminar usuario de la base de datos
        query = "DELETE FROM usuarios WHERE nombre_usuario=%s"
        cursor.execute(query, (usuario_actual,))
        conn.commit()
        messagebox.showinfo("Éxito", "La cuenta ha sido eliminada correctamente.")
        
        # Cerrar las ventanas actuales y mostrar la ventana de login
        ventana_configuracion.destroy()
        ventana_menu.destroy()
        root.deiconify()  # Mostrar la ventana de login
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar la cuenta: {e}")
    finally:
        conn.close()

def modificar_contrasena(usuario_actual, ventana_configuracion, root, ventana_menu):
    def guardar_nueva_contrasena():
        nueva_contrasena = nueva_contrasena_entry.get()
        confirmar_contrasena = confirmar_contrasena_entry.get()

        if nueva_contrasena == "" or confirmar_contrasena == "":
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            limpiar_campos()
            return

        if len(nueva_contrasena) < 8 or len(confirmar_contrasena) < 8:
            messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 8 caracteres.")
            limpiar_campos()
            return

        if nueva_contrasena != confirmar_contrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            limpiar_campos()
            return

        conn = conectar_db()
        cursor = conn.cursor()

        query = "UPDATE usuarios SET contrasena=%s WHERE nombre_usuario=%s"
        try:
            cursor.execute(query, (nueva_contrasena, usuario_actual))
            conn.commit()
            messagebox.showinfo("Éxito", "Contraseña modificada correctamente.")
            ventana_modificar_contrasena.destroy()
            ventana_configuracion.destroy()  # Cerrar la ventana de configuración
            ventana_menu.destroy()
            root.deiconify()  # Mostrar la ventana de login
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error al modificar la contraseña: {e}")
            limpiar_campos()
        finally:
            conn.close()

    def limpiar_campos():
        nueva_contrasena_entry.delete(0, tk.END)
        confirmar_contrasena_entry.delete(0, tk.END)
        
    ventana_modificar_contrasena = Toplevel()
    ventana_modificar_contrasena.title("Modificar Contraseña")
    ventana_modificar_contrasena.geometry("500x300+1+45")
    ventana_modificar_contrasena.configure(bg="ivory2")

    # Quitar botones de minimizar y maximizar
    ventana_modificar_contrasena.attributes('-toolwindow', True) 

    label_titulo = Label(ventana_modificar_contrasena, text="Modificar Contraseña", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 20, "bold"))
    label_titulo.pack(pady=20)
    
    nueva_contrasena_label = Label(ventana_modificar_contrasena, text="Nueva Contraseña:", bg="ivory2", font=("Microsoft YaHei UI Light", 12))
    nueva_contrasena_label.pack(pady=10)
    nueva_contrasena_entry = Entry(ventana_modificar_contrasena, width=30, show='*', font=("Microsoft YaHei UI Light", 12))
    nueva_contrasena_entry.pack()

    confirmar_contrasena_label = Label(ventana_modificar_contrasena, text="Confirmar Contraseña:", bg="ivory2", font=("Microsoft YaHei UI Light", 12))
    confirmar_contrasena_label.pack(pady=10)
    confirmar_contrasena_entry = Entry(ventana_modificar_contrasena, width=30, show='*', font=("Microsoft YaHei UI Light", 12))
    confirmar_contrasena_entry.pack()

    guardar_button = Button(ventana_modificar_contrasena, text="Guardar", width=15, bg="springGreen2", fg="black", font=("Microsoft YaHei UI Light", 12), command=guardar_nueva_contrasena)
    guardar_button.pack(pady=20)

    # Hacer la ventana de perfil modal
    ventana_modificar_contrasena .grab_set()
    ventana_modificar_contrasena .focus_set()
    ventana_modificar_contrasena .wait_window()

    ventana_modificar_contrasena.mainloop()

def mostrar_configuracion(usuario_actual, root, ventana_menu):
    # Hacer la ventana de perfil modal
    ventana_configuracion= Toplevel()
    ventana_configuracion.title("Configuración de Usuario")
    ventana_configuracion.geometry("500x300+1+45")
    ventana_configuracion.configure(bg="ivory2")
    ventana_configuracion.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_configuracion.attributes('-toolwindow', True) 

    Label(ventana_configuracion, text="Configuración de Usuario", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 23, "bold")).pack(pady=20)
    
    frame_principal = Frame(ventana_configuracion, bg="ivory2")
    frame_principal.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
    
    # Parte izquierda: Foto de perfil
    frame_izquierda = Frame(frame_principal, bg="ivory2")
    frame_izquierda.pack(side=tk.LEFT, padx=20)
    
    label_foto = Label(frame_izquierda, bg="ivory2")
    label_foto.pack(pady=10)
    cargar_foto_perfil(label_foto, usuario_actual)
    
    # Parte derecha: Botones
    frame_derecha = Frame(frame_principal, bg="ivory2")
    frame_derecha.pack(side=tk.RIGHT, padx=20)

    btn_cambiar_foto = Button(frame_derecha, width=20, pady=7, text="Cambiar Foto de Perfil", bg="#57a1f8", fg="black", border=0, font=("Microsoft YaHei UI Light", 9), command=lambda: cambiar_foto(label_foto, usuario_actual))
    btn_cambiar_foto.pack(pady=10, padx=10, fill=tk.X)

    btn_modificar_cuenta = Button(frame_derecha, width=20, pady=7, text="Modificar Contraseña", bg="#57a1f8", fg="black", border=0, font=("Microsoft YaHei UI Light", 9), command=lambda: modificar_contrasena(usuario_actual, ventana_configuracion, root, ventana_menu))
    btn_modificar_cuenta.pack(pady=10, padx=10, fill=tk.X)

    btn_eliminar_cuenta = Button(frame_derecha, width=20, pady=7, text="Eliminar Cuenta", bg="#57a1f8", fg="black", border=0, font=("Microsoft YaHei UI Light", 9), command=lambda: eliminar_cuenta(usuario_actual, ventana_configuracion, root, ventana_menu))
    btn_eliminar_cuenta.pack(pady=10, padx=10, fill=tk.X)

    # Hacer la ventana de perfil modal
    ventana_configuracion.grab_set()
    ventana_configuracion.focus_set()
    ventana_configuracion.wait_window()

    ventana_configuracion.mainloop()

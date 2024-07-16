import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, Toplevel
from database.db_connection import conectar_db

def registrar_cliente(nombre_usuario):
    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_cedula.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)

    def guardar_cliente():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        cedula = entry_cedula.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()

        if not nombre or not apellido or not cedula or not correo or not telefono or not direccion:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            limpiar_campos()
            return

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            # Verificar si el usuario ya está registrado como cliente
            query_check_cliente = "SELECT id FROM cliente WHERE id_usuario = (SELECT id FROM usuarios WHERE nombre_usuario = %s)"
            cursor.execute(query_check_cliente, (nombre_usuario,))
            resultado_cliente = cursor.fetchone()

            if resultado_cliente:
                messagebox.showinfo("Información", "El usuario ya está registrado como cliente.")
                limpiar_campos()
                ventana_registrar_cliente.destroy()
                return

            # Verificar el número de clientes registrados bajo el usuario
            query_count_clientes = "SELECT COUNT(*) FROM cliente WHERE id_usuario = (SELECT id FROM usuarios WHERE nombre_usuario = %s)"
            cursor.execute(query_count_clientes, (nombre_usuario,))
            numero_clientes = cursor.fetchone()[0]

            if numero_clientes >= 10:
                messagebox.showwarning("Advertencia", "El usuario ya tiene el máximo de 10 clientes registrados.")
                limpiar_campos()
                return

            # Insertar datos del cliente en la base de datos
            query_insert = "INSERT INTO cliente (id_usuario, nombre, apellido, cedula, correo, telefono, direccion) VALUES ((SELECT id FROM usuarios WHERE nombre_usuario = %s), %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_insert, (nombre_usuario, nombre, apellido, cedula, correo, telefono, direccion))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            limpiar_campos()
            ventana_registrar_cliente.destroy()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")
            limpiar_campos()

        finally:
            conn.close()

    ventana_registrar_cliente = Toplevel()
    ventana_registrar_cliente.title("Registrar Cliente")
    ventana_registrar_cliente.geometry("400x490+1+45")
    ventana_registrar_cliente.configure(bg="ivory2")
    ventana_registrar_cliente.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_registrar_cliente.attributes('-toolwindow', True) 

    Label(ventana_registrar_cliente, text="Registrar Cliente", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 20, "bold")).pack(pady=20)

    frame = tk.Frame(ventana_registrar_cliente, bg="ivory2")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    Label(frame, text="Nombre:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    Label(frame, text="Apellido:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=1, column=0, sticky="w", pady=5)
    entry_apellido = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_apellido.grid(row=1, column=1, padx=5, pady=5)

    Label(frame, text="Cédula:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=2, column=0, sticky="w", pady=5)
    entry_cedula = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_cedula.grid(row=2, column=1, padx=5, pady=5)

    Label(frame, text="Correo:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=3, column=0, sticky="w", pady=5)
    entry_correo = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_correo.grid(row=3, column=1, padx=5, pady=5)

    Label(frame, text="Teléfono:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=4, column=0, sticky="w", pady=5)
    entry_telefono = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_telefono.grid(row=4, column=1, padx=5, pady=5)

    Label(frame, text="Dirección:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=5, column=0, sticky="w", pady=5)
    entry_direccion = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_direccion.grid(row=5, column=1, padx=5, pady=5)

    Button(ventana_registrar_cliente, text="Guardar", width=15, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=guardar_cliente).pack(pady=15)
     
    # Hacer la ventana de perfil modal
    ventana_registrar_cliente.grab_set()
    ventana_registrar_cliente.focus_set()
    ventana_registrar_cliente.wait_window()

    ventana_registrar_cliente.mainloop()
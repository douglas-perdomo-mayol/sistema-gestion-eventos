import tkinter as tk
from tkinter import messagebox, ttk
from database.db_connection import conectar_db

def cargar_eventos(tree, nombre_cliente):
    # Limpiar Treeview antes de cargar nuevos eventos
    for item in tree.get_children():
        tree.delete(item)

    if not nombre_cliente:
        messagebox.showwarning("Advertencia", "Nombre de usuario no válido.")
        return

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        # Consulta SQL para seleccionar eventos por el nombre del usuario
        query = """
        SELECT e.id, e.nombre, e.descripcion, e.fecha_inicio, e.fecha_final, e.ubicacion, e.tipo, e.capacidad, e.precio, e.estado 
        FROM evento e
        JOIN cliente c ON e.id_cliente = c.id
        WHERE c.nombre = %s
        """
        cursor.execute(query, (nombre_cliente,))
        eventos = cursor.fetchall()

        # Mostrar eventos en el Treeview
        for evento in eventos:
            tree.insert("", tk.END, values=evento)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo consultar los eventos: {e}")

    finally:
        conn.close()

def consultar_eventos(nombre_usuario):
    ventana_consulta = tk.Toplevel()
    ventana_consulta.title("Consultar Eventos")
    ventana_consulta.geometry("800x500+1+45")
    ventana_consulta.configure(bg="ivory2")
    ventana_consulta.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_consulta.attributes('-toolwindow', True) 

    # Crear un Treeview para mostrar los eventos
    columns = ("ID", "Nombre", "Descripción", "Fecha Inicio", "Fecha Final", "Ubicación", "Tipo", "Capacidad", "Precio", "Estado")
    tree = ttk.Treeview(ventana_consulta, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)

    tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Función para cargar los eventos al Treeview
    def on_cargar_eventos():
        nombre_usuario = input_nombre_usuario.get()  # Obtener nombre de usuario del Entry
        if not nombre_usuario:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre de usuario.")
            return

        cargar_eventos(tree, nombre_usuario)

    # Entrada para el nombre de usuario
    frame_nombre_usuario = tk.Frame(ventana_consulta, bg="ivory2")
    frame_nombre_usuario.pack(fill=tk.X, padx=20, pady=10)

    tk.Label(frame_nombre_usuario, text="Nombre de Cliente:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).pack(side=tk.LEFT, padx=10)
    input_nombre_usuario = tk.Entry(frame_nombre_usuario, width=30, font=("Microsoft YaHei UI Light", 12))
    input_nombre_usuario.pack(side=tk.LEFT, padx=10)

    # Botón para cargar los eventos
    btn_cargar_eventos = tk.Button(ventana_consulta, text="Cargar Eventos", width=20, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=on_cargar_eventos)
    btn_cargar_eventos.pack(pady=20)

    # Agregar Scrollbars
    scrollbar_y = ttk.Scrollbar(ventana_consulta, orient=tk.VERTICAL, command=tree.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(ventana_consulta, orient=tk.HORIZONTAL, command=tree.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=scrollbar_x.set)

    # Hacer la ventana de perfil modal
    ventana_consulta.grab_set()
    ventana_consulta.focus_set()
    ventana_consulta.wait_window()

    ventana_consulta.mainloop()
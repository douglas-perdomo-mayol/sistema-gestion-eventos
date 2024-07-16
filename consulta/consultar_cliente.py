import tkinter as tk
from tkinter import messagebox, ttk
from database.db_connection import conectar_db

def cargar_clientes(tree):
    # Limpiar Treeview antes de cargar nuevos clientes
    for item in tree.get_children():
        tree.delete(item)

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        # Consulta SQL para seleccionar todos los clientes
        query = "SELECT id, nombre, telefono, direccion  FROM cliente"
        cursor.execute(query)
        clientes = cursor.fetchall()

        # Mostrar clientes en el Treeview
        for cliente in clientes:
            tree.insert("", tk.END, values=cliente)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo consultar los clientes: {e}")

    finally:
        conn.close()

def consultar_clientes():
    ventana_consulta = tk.Toplevel()
    ventana_consulta.title("Consultar Clientes")
    ventana_consulta.geometry("800x500+1+45")
    ventana_consulta.configure(bg="ivory2")
    ventana_consulta.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_consulta.attributes('-toolwindow', True) 

    # Crear un Treeview para mostrar los clientes
    columns = ("ID", "Nombre", "Teléfono", "Dirección")
    tree = ttk.Treeview(ventana_consulta, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor=tk.CENTER)

    tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Función para cargar los clientes al Treeview
    def on_cargar_clientes():
        cargar_clientes(tree)

    # Botón para cargar los clientes
    btn_cargar_clientes = tk.Button(ventana_consulta, text="Cargar Clientes", width=20, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=on_cargar_clientes)
    btn_cargar_clientes.pack(pady=20)

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
    # Iniciar con el Treeview vacío
    ventana_consulta.mainloop()
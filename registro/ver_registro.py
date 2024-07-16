import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import conectar_db

def ver_registro():
    def toggle_mostrar_contrasenas():
        # Mostrar contraseñas si el Checkbutton está marcado, de lo contrario, ocultarlas
        mostrar = mostrar_contrasenas.get()
        if mostrar:
            tree.heading("Contraseña", text="Contraseña")
        else:
            tree.heading("Contraseña", text="**********")

        cargar_registros()  # Recargar los registros para aplicar los cambios

    def cargar_registros():
        for row in tree.get_children():
            tree.delete(row)

        conn = conectar_db()
        cursor = conn.cursor()

        query = "SELECT id, nombre_usuario, contrasena FROM usuarios"
        cursor.execute(query)
        resultados = cursor.fetchall()

        for resultado in resultados:
            if not mostrar_contrasenas.get():  # Si no se debe mostrar la contraseña
                resultado = (resultado[0], resultado[1], "**********")
            tree.insert('', 'end', values=resultado)

        conn.close()

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Ver Registro")
    ventana_registro.geometry("925x500+1+45")
    ventana_registro.configure(bg="ivory2")
    ventana_registro.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_registro.attributes('-toolwindow', True) 

    # Crear un frame para el árbol y las barras de desplazamiento
    frame = tk.Frame(ventana_registro, bg="ivory2")
    frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Crear el árbol
    tree = ttk.Treeview(frame, columns=("ID", "Nombre Usuario", "Contraseña"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Nombre Usuario", text="Nombre Usuario")
    tree.heading("Contraseña", text="**********")  # Inicialmente mostrar contraseñas ocultas
    tree.grid(row=0, column=0, sticky='nsew')

    # Crear las barras de desplazamiento
    scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
    
    # Configurar el árbol para usar las barras de desplazamiento
    tree.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Posicionar las barras de desplazamiento
    scrollbar_y.grid(row=0, column=1, sticky='ns')
    scrollbar_x.grid(row=1, column=0, sticky='ew')

    # Ajustar el frame para que cambie de tamaño con la ventana
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Crear un Checkbutton para permitir mostrar las contraseñas
    mostrar_contrasenas = tk.BooleanVar()
    mostrar_contrasenas.set(False)  # Inicialmente no mostrar las contraseñas
    check_mostrar_contrasenas = tk.Checkbutton(ventana_registro, text="Mostrar Contraseñas", variable=mostrar_contrasenas, command=toggle_mostrar_contrasenas)
    check_mostrar_contrasenas.pack()

    # Crear un botón para cargar los registros
    boton_cargar = tk.Button(ventana_registro, text="Cargar Registros", width=20, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=cargar_registros)
    boton_cargar.pack(pady=10)

    # Hacer la ventana de perfil modal
    ventana_registro.grab_set()
    ventana_registro.focus_set()
    ventana_registro.wait_window()

    ventana_registro.mainloop()
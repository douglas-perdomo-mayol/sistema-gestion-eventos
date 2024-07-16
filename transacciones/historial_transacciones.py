import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, Toplevel
from tkinter.ttk import Treeview, Scrollbar
from database.db_connection import conectar_db

def historial_transacciones(nombre_usuario):
    def cargar_historial():
        nombre_cliente = entry_nombre_cliente.get()
        if not nombre_cliente:
            messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del cliente.")
            return

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            # Obtener el id_cliente del nombre del cliente ingresado
            query_cliente = "SELECT id FROM cliente WHERE nombre = %s"
            cursor.execute(query_cliente, (nombre_cliente,))
            cliente = cursor.fetchone()

            if not cliente:
                messagebox.showinfo("Información", "Cliente no registrado.")
                return

            id_cliente = cliente[0]

            # Limpiar resultados no leídos
            cursor.fetchall()

            # Consulta para obtener el historial de transacciones
            query_transacciones = """
            SELECT id, id_evento, fecha, monto_pagado, metodo_pago, estado_transaccion 
            FROM transacciones 
            WHERE id_cliente = %s
            """
            cursor.execute(query_transacciones, (id_cliente,))
            transacciones = cursor.fetchall()

            # Limpiar el Treeview antes de cargar nuevas transacciones
            for item in tree.get_children():
                tree.delete(item)

            if not transacciones:
                messagebox.showinfo("Información", "El cliente no tiene ninguna transacción por el momento.")
                return

            total_monto_pagado = sum(transaccion[3] for transaccion in transacciones)

            # Insertar filas en el Treeview
            for transaccion in transacciones:
                tree.insert("", "end", values=transaccion)

            # Mostrar el total del monto pagado
            label_total_monto.config(text=f"Total Monto Pagado: ${total_monto_pagado:.2f}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al recuperar el historial de transacciones: {e}")
        
        finally:
            conn.close()

    ventana_historial = Toplevel()
    ventana_historial.title("Historial de Transacciones")
    ventana_historial.geometry("850x650+1+45")
    ventana_historial.configure(bg="ivory2")
    ventana_historial.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_historial.attributes('-toolwindow', True)

    Label(ventana_historial, text="Historial de Transacciones", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 20, "bold")).pack(pady=20)

    frame_cliente = tk.Frame(ventana_historial, bg="ivory2")
    frame_cliente.pack(pady=3)

    Label(frame_cliente, text="Nombre de Cliente:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=0, column=0, sticky="w", padx=10)
    entry_nombre_cliente = Entry(frame_cliente, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_nombre_cliente.grid(row=0, column=1, padx=10)
    Button(frame_cliente, text="Cargar Historial", width=15, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=cargar_historial).grid(row=0, column=2, padx=10)

    # Crear Treeview para mostrar el historial
    columns = ("ID", "Evento", "Fecha", "Monto Pagado", "Método de Pago", "Estado")
    tree = Treeview(ventana_historial, columns=columns, show="headings", height=20)

    # Configurar encabezados
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    # Crear Scrollbars
    scrollbar_y = Scrollbar(ventana_historial, orient=tk.VERTICAL, command=tree.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = Scrollbar(ventana_historial, orient=tk.HORIZONTAL, command=tree.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=scrollbar_x.set)

    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Mostrar el total del monto pagado
    label_total_monto = Label(ventana_historial, text=f"Total Monto Pagado: $0.00", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 16, "bold"))
    label_total_monto.pack(pady=10)

    # Hacer la ventana de perfil modal
    ventana_historial.grab_set()
    ventana_historial.focus_set()
    ventana_historial.wait_window()

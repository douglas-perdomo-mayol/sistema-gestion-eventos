import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, Toplevel
from tkinter.ttk import Combobox, Treeview, Scrollbar
from tkcalendar import DateEntry
from database.db_connection import conectar_db

def registrar_evento(nombre_usuario, ventana_menu):
    def guardar_evento():
        nombre_cliente = entry_nombre_cliente.get()
        nombre = entry_nombre.get()
        descripcion = entry_descripcion.get()
        fecha_inicio = entry_fecha_inicio.get_date()
        hora_inicio = f"{combobox_hora_inicio.get()}:{combobox_minuto_inicio.get()}:00"
        fecha_final = entry_fecha_final.get_date()
        hora_final = f"{combobox_hora_final.get()}:{combobox_minuto_final.get()}:00"
        ubicacion = entry_ubicacion.get()
        tipo = combobox_tipo.get()
        capacidad = combobox_capacidad.get()
        precio_descripcion = combobox_precio.get()
        precio = precios_descripciones.get(precio_descripcion)
        estado = combobox_estado.get()

        # Verificar si algún campo obligatorio está vacío
        if not nombre_cliente or not nombre or not descripcion or not fecha_inicio or not fecha_final or not hora_inicio or not hora_final or not ubicacion or not tipo or not capacidad or not precio or not estado:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            return

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            # Verificar si el cliente está registrado
            query_check_cliente = "SELECT id FROM cliente WHERE nombre = %s"
            cursor.execute(query_check_cliente, (nombre_cliente,))
            resultado_cliente = cursor.fetchone()

            if not resultado_cliente:
                messagebox.showerror("Error", "El cliente no está registrado.")
                return

            # Si el cliente está registrado, procedemos a guardar el evento
            query_insert = "INSERT INTO evento (id_cliente, nombre, descripcion, fecha_inicio, fecha_final, hora_inicio, hora_final, ubicacion, tipo, capacidad, precio, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_insert, (resultado_cliente[0], nombre, descripcion, fecha_inicio, fecha_final, hora_inicio, hora_final, ubicacion, tipo, capacidad, precio, estado))
            conn.commit()
            messagebox.showinfo("Éxito", "Evento registrado correctamente.")
            ventana_registrar_evento.destroy()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo registrar el evento: {e}")

        finally:
            conn.close()

    def mostrar_registros_eventos():
        def visualizar_eventos():
            nombre_cliente = entry_nombre_cliente.get()
            if not nombre_cliente:
                messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del cliente.")
                return

            conn = conectar_db()
            cursor = conn.cursor()

            try:
                # Limpiar la tabla antes de insertar nuevos registros
                for item in tree.get_children():
                    tree.delete(item)

                # Consulta para obtener los eventos del cliente especificado
                query = """
                    SELECT evento.id, evento.nombre, evento.precio, evento.estado_pago
                    FROM evento
                    JOIN cliente ON evento.id_cliente = cliente.id
                    WHERE cliente.nombre = %s
                """
                cursor.execute(query, (nombre_cliente,))
                eventos = cursor.fetchall()

                # Insertar filas en el Treeview
                for evento in eventos:
                    id_evento = evento[0]
                    nombre = evento[1]
                    precio = evento[2]
                    estado_transaccion = evento[3]

                    tree.insert("", tk.END, values=(id_evento, nombre, precio, estado_transaccion))

            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar los eventos: {e}")

            finally:
                conn.close()

        ventana_registros = Toplevel(ventana_menu)
        ventana_registros.title("Eventos Registrados")
        ventana_registros.geometry("800x500+1+45")
        ventana_registros.configure(bg="white")
        ventana_registros.resizable(False, False)

        # Quitar botones de minimizar y maximizar
        ventana_registros.attributes('-toolwindow', True)

        Label(ventana_registros, text="Nombre del Cliente:", bg="white", font=("Microsoft YaHei UI Light", 12)).pack(pady=10)
        entry_nombre_cliente = Entry(ventana_registros, width=30, font=("Microsoft YaHei UI Light", 12))
        entry_nombre_cliente.pack(pady=5)

        Button(ventana_registros, text="Mostrar Eventos", width=20, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=visualizar_eventos).pack(pady=10)

        # Crear Treeview para mostrar los eventos
        columns = ("ID", "Nombre de Evento", "Precio", "Estado De Pago")
        tree = Treeview(ventana_registros, columns=columns, show="headings")

        # Configurar encabezados
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        # Crear Scrollbars
        scrollbar_y = Scrollbar(ventana_registros, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(ventana_registros, orient=tk.HORIZONTAL, command=tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=scrollbar_x.set)

        # Posicionar el Treeview con barras de desplazamiento
        tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Hacer la ventana de perfil modal
        ventana_registros.grab_set()
        ventana_registros.focus_set()
        ventana_registros.wait_window()
  
    ventana_registrar_evento = Toplevel(ventana_menu)
    ventana_registrar_evento.title("Registrar Evento")
    ventana_registrar_evento.geometry("925x550+1+45")
    ventana_registrar_evento.configure(bg="ivory2")
    ventana_registrar_evento.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_registrar_evento.attributes('-toolwindow', True) 

    Label(ventana_registrar_evento, text="Registrar Evento", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 20, "bold")).pack(pady=20)

    Button(ventana_registrar_evento, text="Mostrar Eventos Registrados", width=30, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=mostrar_registros_eventos).pack(pady=20)

    frame = tk.Frame(ventana_registrar_evento, bg="ivory2")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Frame para la izquierda
    left_frame = tk.Frame(frame, bg="ivory2")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    Label(left_frame, text="Nombre de Cliente:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre_cliente= Entry(left_frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=5)

    Label(left_frame, text="Nombre:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=1, column=0, sticky="w", pady=5)
    entry_nombre = Entry(left_frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_nombre.grid(row=1, column=1, padx=5, pady=5)

    Label(left_frame, text="Descripción:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=2, column=0, sticky="w", pady=5)
    entry_descripcion = Entry(left_frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_descripcion.grid(row=2, column=1, padx=5, pady=5)

    Label(left_frame, text="Fecha de Inicio:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=3, column=0, sticky="w", pady=5)
    entry_fecha_inicio = DateEntry(left_frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_fecha_inicio.grid(row=3, column=1, padx=5, pady=5)

    Label(left_frame, text="Hora de Inicio:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=4, column=0, sticky="w", pady=5)
    combobox_hora_inicio = Combobox(left_frame, values=[f"{i:02d}" for i in range(24)], width=5, font=("Microsoft YaHei UI Light", 12))
    combobox_hora_inicio.grid(row=4, column=1, sticky="w", padx=(5, 0))
    combobox_minuto_inicio = Combobox(left_frame, values=[f"{i:02d}" for i in range(60)], width=5, font=("Microsoft YaHei UI Light", 12))
    combobox_minuto_inicio.grid(row=4, column=1, padx=(60, 5))

    Label(left_frame, text="Fecha de Finalización:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=5, column=0, sticky="w", pady=5)
    entry_fecha_final = DateEntry(left_frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_fecha_final.grid(row=5, column=1, padx=5, pady=5)

    Label(left_frame, text="Hora de Finalización:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=6, column=0, sticky="w", pady=5)
    combobox_hora_final = Combobox(left_frame, values=[f"{i:02d}" for i in range(24)], width=5, font=("Microsoft YaHei UI Light", 12))
    combobox_hora_final.grid(row=6, column=1, sticky="w", padx=(5, 0))
    combobox_minuto_final = Combobox(left_frame, values=[f"{i:02d}" for i in range(60)], width=5, font=("Microsoft YaHei UI Light", 12))
    combobox_minuto_final.grid(row=6, column=1, padx=(60, 5))

    # Right frame components
    right_frame = tk.Frame(frame, bg="ivory2")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

    Label(right_frame, text="Ubicación:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=0, column=0, sticky="w", pady=5)
    entry_ubicacion = Entry(right_frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_ubicacion.grid(row=0, column=1, padx=5, pady=5)

    Label(right_frame, text="Tipo:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=1, column=0, sticky="w", pady=5)
    tipos_evento = ["Conferencia", "Seminario", "Taller", "Otro"]
    combobox_tipo = Combobox(right_frame, values=tipos_evento, width=27, font=("Microsoft YaHei UI Light", 12))
    combobox_tipo.grid(row=1, column=1, padx=5, pady=5)

    Label(right_frame, text="Capacidad:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=2, column=0, sticky="w", pady=5)
    capacidades = [100, 200, 300, 400, 500]
    combobox_capacidad = Combobox(right_frame, values=capacidades, width=27, font=("Microsoft YaHei UI Light", 12))
    combobox_capacidad.grid(row=2, column=1, padx=5, pady=5)

    Label(right_frame, text="Precio:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=3, column=0, sticky="w", pady=5)
    precios_descripciones = {
        "1-2 horas 1000": 1000,
        "3-5 horas 5000": 5000,
        "6-8 horas 9000": 9000,
        "8+ horas 15000": 15000
    }
    precios = list(precios_descripciones.keys())
    combobox_precio = Combobox(right_frame, values=precios, width=27, font=("Microsoft YaHei UI Light", 12))
    combobox_precio.grid(row=3, column=1, padx=5, pady=5)

    Label(right_frame, text="Estado:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=4, column=0, sticky="w", pady=5)
    estados_evento = ["Activo", "Cancelado", "Pendiente", "Finalizado"]
    combobox_estado = Combobox(right_frame, values=estados_evento, width=27, font=("Microsoft YaHei UI Light", 12))
    combobox_estado.grid(row=4, column=1, padx=5, pady=5)

    # Botón para guardar el evento
    Button(ventana_registrar_evento, text="Crear Evento", width=30, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=guardar_evento).pack(pady=20)

    # Hacer la ventana de perfil modal
    ventana_registrar_evento.grab_set()
    ventana_registrar_evento.focus_set()
    ventana_registrar_evento.wait_window()
import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, Toplevel
from tkinter.ttk import Combobox
from datetime import datetime
from database.db_connection import conectar_db

def nueva_transferencia(nombre_usuario, ventana_menu):
    def cargar_eventos():
        nombre_cliente = entry_nombre_cliente.get()
        if not nombre_cliente:
            messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del cliente.")
            return
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        try:
            # Obtener el ID del cliente
            query_cliente = "SELECT id FROM cliente WHERE nombre = %s"
            cursor.execute(query_cliente, (nombre_cliente,))
            resultado_cliente = cursor.fetchone()

            if not resultado_cliente:
                messagebox.showerror("Error", "No se encontró el cliente en la base de datos.")
                return

            id_cliente = resultado_cliente[0]

            # Obtener los eventos asociados al cliente
            query_eventos = "SELECT id, nombre FROM evento WHERE id_cliente = %s"
            cursor.execute(query_eventos, (id_cliente,))
            eventos = cursor.fetchall()

            if not eventos:
                messagebox.showerror("Error", "No se encontraron eventos asociados al cliente.")
                return

            # Limpiar el combobox de eventos y agregar los eventos obtenidos
            combobox_evento["values"] = [f"{evento[0]} - {evento[1]}" for evento in eventos]
            combobox_evento.current(0)  # Seleccionar el primer evento por defecto

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los eventos: {e}")

        finally:
            conn.close()

    def guardar_transaccion():
        nombre_cliente = entry_nombre_cliente.get()
        evento_seleccionado = combobox_evento.get()
        monto_pagado = entry_monto_pagado.get()
        fecha_transaccion = entry_fecha_transaccion.get()
        metodo_pago = combobox_metodo_pago.get()
        estado_transaccion = combobox_estado_transaccion.get()

        if not nombre_cliente or not evento_seleccionado or not monto_pagado or not fecha_transaccion or not metodo_pago or not estado_transaccion:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
            return

        try:
            monto_pagado = float(monto_pagado)
        except ValueError:
            messagebox.showwarning("Advertencia", "El monto pagado debe ser un número.")
            return

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            # Obtener el ID del cliente
            query_cliente = "SELECT id FROM cliente WHERE nombre = %s"
            cursor.execute(query_cliente, (nombre_cliente,))
            resultado_cliente = cursor.fetchone()

            if not resultado_cliente:
                messagebox.showerror("Error", "No se encontró el cliente en la base de datos.")
                return

            id_cliente = resultado_cliente[0]

            # Obtener el ID y el precio del evento seleccionado
            id_evento = int(evento_seleccionado.split(" - ")[0])
            query_precio_evento = "SELECT precio FROM evento WHERE id = %s"
            cursor.execute(query_precio_evento, (id_evento,))
            resultado_evento = cursor.fetchone()

            if not resultado_evento:
                messagebox.showerror("Error", "No se encontró el evento en la base de datos.")
                return

            precio_total = resultado_evento[0]

            # Convertir la fecha ingresada a formato DATE de MySQL
            fecha_transaccion = datetime.strptime(fecha_transaccion, "%Y-%m-%d").date()

            # Insertar la transacción
            query_insert = "INSERT INTO transacciones (id_cliente, id_evento, fecha, monto_pagado, metodo_pago, estado_transaccion) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query_insert, (id_cliente, id_evento, fecha_transaccion, monto_pagado, metodo_pago, estado_transaccion))
            conn.commit()

            # Comprobar si el monto pagado cubre el precio total del evento
            if monto_pagado >= precio_total:
                # Actualizar el estado de pago del evento a 'pagado'
                query_update_evento = "UPDATE evento SET estado_pago = 'pagado' WHERE id = %s"
                cursor.execute(query_update_evento, (id_evento,))
                conn.commit()
                messagebox.showinfo("Éxito", "Transacción registrada. El evento ha sido pagado por completo.")
            else:
                restante = precio_total - monto_pagado
                query_update_evento = "UPDATE evento SET estado_pago = 'pendiente' WHERE id = %s"
                cursor.execute(query_update_evento, (id_evento,))
                conn.commit()
                messagebox.showinfo("Información", f"Transacción registrada. Falta por pagar: ${restante:.2f}")

            ventana_nueva_transferencia.destroy()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo registrar la transacción: {e}")

        finally:
            conn.close()

    ventana_nueva_transferencia = Toplevel(ventana_menu)
    ventana_nueva_transferencia.title("Nueva Transacción")
    ventana_nueva_transferencia.geometry("900x560+1+45")
    ventana_nueva_transferencia.configure(bg="ivory2")
    ventana_nueva_transferencia.resizable(False, False)

    # Quitar botones de minimizar y maximizar
    ventana_nueva_transferencia.attributes('-toolwindow', True)

    Label(ventana_nueva_transferencia, text="Nueva Transacción", fg="#57a1f8", bg="ivory2", font=("Microsoft YaHei UI Light", 20, "bold")).pack(pady=20)

    frame = tk.Frame(ventana_nueva_transferencia, bg="ivory2")
    frame.pack(padx=20, pady=20)

    Label(frame, text="Nombre de Cliente:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=0, column=0, sticky="w", pady=10)
    entry_nombre_cliente = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_nombre_cliente.grid(row=0, column=1, padx=10, pady=10)

    Button(frame, text="Cargar Eventos", width=15, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=cargar_eventos).grid(row=0, column=2, padx=10, pady=10)

    Label(frame, text="Evento:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=1, column=0, sticky="w", pady=10)
    combobox_evento = Combobox(frame, width=27, font=("Microsoft YaHei UI Light", 12))
    combobox_evento.grid(row=1, column=1, padx=10, pady=10)

    Label(frame, text="Monto Pagado:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=2, column=0, sticky="w", pady=10)
    entry_monto_pagado = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_monto_pagado.grid(row=2, column=1, padx=10, pady=10)

    Label(frame, text="Fecha Transacción (YYYY-MM-DD):", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=3, column=0, sticky="w", pady=10)
    entry_fecha_transaccion = Entry(frame, width=30, font=("Microsoft YaHei UI Light", 12))
    entry_fecha_transaccion.grid(row=3, column=1, padx=10, pady=10)

    Label(frame, text="Método de Pago:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=4, column=0, sticky="w", pady=10)
    metodos_pago = ["Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia Bancaria", "PayPal", "Otro"]
    combobox_metodo_pago = Combobox(frame, values=metodos_pago, width=27, font=("Microsoft YaHei UI Light", 12))
    combobox_metodo_pago.grid(row=4, column=1, padx=10, pady=10)

    Label(frame, text="Estado Transacción:", bg="ivory2", font=("Microsoft YaHei UI Light", 12)).grid(row=5, column=0, sticky="w", pady=10)
    estados_transaccion = ["Pendiente", "Completado", "Rechazado"]
    combobox_estado_transaccion = Combobox(frame, values=estados_transaccion, width=27, font=("Microsoft YaHei UI Light", 12))
    combobox_estado_transaccion.grid(row=5, column=1, padx=10, pady=10)

    Button(ventana_nueva_transferencia, text="Guardar", width=15, bg="#57a1f8", fg="black", font=("Microsoft YaHei UI Light", 12), command=guardar_transaccion).pack(pady=20)

    # Hacer la ventana de perfil modal
    ventana_nueva_transferencia.grab_set()
    ventana_nueva_transferencia.focus_set()
    ventana_nueva_transferencia.wait_window()

    ventana_nueva_transferencia.mainloop()

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from database.db_connection import conectar_db

# Función para cargar datos desde la base de datos
def cargar_datos(nombre_cliente):
    conn = conectar_db()
    cursor = conn.cursor()

    # Consulta para obtener transacciones y eventos del cliente
    query = """
    SELECT 
        t.fecha AS fecha_transaccion,
        t.monto_pagado,
        t.metodo_pago,
        e.nombre AS nombre_evento,
        e.fecha_inicio,
        e.fecha_final
    FROM 
        transacciones t
    JOIN 
        evento e ON t.id_evento = e.id
    JOIN 
        cliente c ON t.id_cliente = c.id
    JOIN 
        usuarios u ON c.id_usuario = u.id
    WHERE 
        c.nombre = %s
    """
    cursor.execute(query, (nombre_cliente,))
    resultados = cursor.fetchall()

    if not resultados:
        conn.close()
        return None

    # Convertir los resultados en un DataFrame de Pandas
    columnas = ['Fecha Transacción', 'Monto Pagado', 'Método de Pago', 'Nombre Evento', 'Fecha Inicio Evento', 'Fecha Fin Evento']
    df = pd.DataFrame(resultados, columns=columnas)
    
    conn.close()
    return df

# Función para generar el informe en PDF
def generar_informe_cliente(nombre_cliente):
    # Cargar datos
    df = cargar_datos(nombre_cliente)
    if df is None or df.empty:
        messagebox.showinfo("Información", f"No se encontraron eventos ni transacciones para el cliente '{nombre_cliente}'.")
        return

    # Pedir al usuario que seleccione la ubicación y nombre del archivo para guardar el PDF
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    pdf_filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Guardar informe como",
        initialfile=f"Informe_{nombre_cliente.replace(' ', '_')}.pdf"
    )

    if not pdf_filename:
        return  # El usuario canceló el diálogo de guardar

    # Crear un documento PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []

    # Estilos para los párrafos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=1))

    # Título del informe
    title = f"Informe de Eventos y Transacciones para el Cliente: {nombre_cliente}"
    story.append(Paragraph(title, styles['Title']))

    # Convertir datos del cliente en un formato de tabla para el PDF
    table_data = [list(df.columns)] + df.values.tolist()

    # Crear tabla para el PDF
    table = Table(table_data, colWidths=[100]*len(df.columns))
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    story.append(table)

    # Generar el PDF
    doc.build(story)
    messagebox.showinfo("Éxito", f"Informe generado: {pdf_filename}")

# Función para pedir el nombre del cliente y generar el informe
def solicitar_nombre_cliente():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    nombre_cliente = simpledialog.askstring("Input", "Ingrese el nombre del cliente:")
    if nombre_cliente:
        generar_informe_cliente(nombre_cliente)
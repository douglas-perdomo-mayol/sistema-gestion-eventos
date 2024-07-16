from tkinter import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database.db_connection import conectar_db
from usuario.perfil import mostrar_perfil
from registrar.registrar_cliente import registrar_cliente
from registrar.registrar_evento import registrar_evento
from transacciones.nueva_transaccion import nueva_transferencia
from transacciones.historial_transacciones import historial_transacciones
from consulta.consultar_cliente import consultar_clientes
from consulta.consultar_evento import consultar_eventos
from registro.ver_registro import ver_registro
from utilidades.configuraciones import mostrar_configuracion
from utilidades.generar_informe import solicitar_nombre_cliente 

usuario_actual = None
ventana_menu = None  # Definir variable global para la ventana del menú principal


def verificar_credenciales():
    global usuario_actual 
    usuario = user.get()
    contrasena = cont.get()
    user.delete(0, "end")
    cont.delete(0, "end")
    
    if usuario == "Usuario" or contrasena == "Contraseña":
        messagebox.showwarning("Advertencia", "Por favor ingrese su usuario y contraseña")
        return
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM usuarios WHERE nombre_usuario=%s AND contrasena=%s"
    cursor.execute(query, (usuario, contrasena))
    resultado = cursor.fetchone()
    fecha = datetime.now().strftime("%Y-%m-%d")
    if resultado:
        # Guarda el id del usuario como un entero en usuario_actual
        usuario_actual = resultado[0]
        usuario_actual = usuario
        messagebox.showinfo("Éxito", f"¡Hola {usuario_actual}, bienvenido a nuestro sistema! Inicio de sesión el {fecha}")
        root.withdraw()  # Ocultar la ventana de login
        mostrar_menu_principal()  # Mostrar el menú principal
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        user.delete(0, "end")
        cont.delete(0, "end")
        user.insert(0, "Usuario")
        cont.insert(0, "Contraseña")
    
    conn.close()


def registrar_usuario():
    usuario = user_reg.get()
    contrasena = cont_reg.get()
    confirmar_contrasena = contfrom.get()
    
    if len(usuario) > 20:
        messagebox.showwarning("Advertencia", "El nombre de usuario debe tener maximo 20 caracteres")
        user_reg.delete(0, "end")
        cont_reg.delete(0, "end")
        contfrom.delete(0, "end")
        user_reg.insert(0, "Usuario")
        cont_reg.insert(0, "Contraseña")
        contfrom.insert(0, "Confirmar Contraseña")
        ventana_registro.lift()
        return
    
    if len(contrasena) < 8:
        messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 8 caracteres")
        user_reg.delete(0, "end")
        cont_reg.delete(0, "end")
        contfrom.delete(0, "end")
        user_reg.insert(0, "Usuario")
        cont_reg.insert(0, "Contraseña")
        contfrom.insert(0, "Confirmar Contraseña")
        ventana_registro.lift()
        return
    
    if usuario == "Usuario" or contrasena == "Contraseña" or confirmar_contrasena == "Confirmar Contraseña":
        messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
        user_reg.delete(0, "end")
        cont_reg.delete(0, "end")
        contfrom.delete(0, "end")
        user_reg.insert(0, "Usuario")
        cont_reg.insert(0, "Contraseña")
        contfrom.insert(0, "Confirmar Contraseña")
        ventana_registro.lift()
        return
    
    if contrasena != confirmar_contrasena:
        messagebox.showerror("Error", "Las contraseñas no coinciden")
        user_reg.delete(0, "end")
        cont_reg.delete(0, "end")
        contfrom.delete(0, "end")
        user_reg.insert(0, "Usuario")
        cont_reg.insert(0, "Contraseña")
        contfrom.insert(0, "Confirmar Contraseña")
        ventana_registro.lift()
        return
    
    # Continuar con el registro si todas las validaciones pasan
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)"
    try:
        cursor.execute(query, (usuario, contrasena))
        conn.commit()
        messagebox.showinfo("Éxito", "Registro exitoso")
        ventana_registro.destroy()  # Cerrar ventana de registro
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error al registrar el usuario: {e}")
        user_reg.delete(0, "end")
        cont_reg.delete(0, "end")
        contfrom.delete(0, "end")
        user_reg.insert(0, "Usuario")
        cont_reg.insert(0, "Contraseña")
        contfrom.insert(0, "Confirmar Contraseña")
        ventana_registro.lift()

    conn.close()


def mostrar_bienvenida():
    ventana_bienvenida = tk.Toplevel(root)
    ventana_bienvenida.overrideredirect(True)
    ventana_bienvenida.geometry('925x500+250+130')
    ventana_bienvenida.configure(bg='white')

    tk.Label(ventana_bienvenida, text="Bienvenido al Sistema de Gestión de Eventos", font=("Microsoft YaHei UI Light", 23, "bold"), bg='white').pack(expand=True)
    
     # Cargar la imagen y ajustar tamaño
    imagen_inicial = PhotoImage(file="img\\evento.png").subsample(9)

    # Mostrar imagen en un Label con tamaño específico
    label_imagen_inicial = Label(ventana_bienvenida, image=imagen_inicial, width=200, height=200, bg='white')
    label_imagen_inicial.image = imagen_inicial  # Guardar referencia a la imagen
    label_imagen_inicial.pack(pady=10)

    # Crear un canvas para dibujar el círculo giratorio
    canvas = tk.Canvas(ventana_bienvenida, width=100, height=100, bg='white', highlightthickness=0)
    canvas.pack(pady=20)
    
    arc = canvas.create_arc((10, 10, 90, 90), start=0, extent=150, outline='#57a1f8', style='arc', width=5)

    def rotate_circle(angle=0):
        canvas.itemconfig(arc, start=angle)
        ventana_bienvenida.after(50, rotate_circle, (angle + 5) % 360)

    rotate_circle()
    
    ventana_bienvenida.after(5000, lambda: (ventana_bienvenida.destroy(), mostrar_login()))  # Mostrar por 5 segundos y luego mostrar login

def mostrar_login():
    global root
    root.deiconify()  # Mostrar la ventana principal

# Función para mostrar el formulario de registro de cliente
def mostrar_registro_cliente():
    registrar_cliente(usuario_actual)

# Función para mostrar el formulario de registro de evento
def mostrar_formulario_evento():
    registrar_evento(usuario_actual, ventana_menu)

# Función para mostrar el formulario de trasacciones
def mostrar_formulario_transacciones():
    nueva_transferencia(usuario_actual,ventana_menu)

def mostrar_historial_transacciones():
    historial_transacciones(usuario_actual)  

def mostrar_consultar_clientes():
    consultar_clientes() 

def mostrar_consultar_eventos():
    consultar_eventos(usuario_actual)



def mostrar_registro():
    global ventana_registro, user_reg, cont_reg, contfrom
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registrar")
    ventana_registro.geometry("925x500+250+130")
    ventana_registro.configure(bg="#fff")
    ventana_registro.resizable(False, False)
    
    img = PhotoImage(file="img\\registrar.png")
    label_img = Label(ventana_registro, image=img, border=0, bg="white")
    label_img.image = img  # Guardar referencia a la imagen
    label_img.place(x=50, y=90)

    frame = Frame(ventana_registro, width=350, height=390, bg="#fff")
    frame.place(x=480, y=50)

    heading = Label(frame, text="Registrar", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
    heading.place(x=100, y=5)

    def on_enter(e):
        user_reg.delete(0, "end")
    def on_leave(e):
        name = user_reg.get()
        if name == "":
            user_reg.insert(0, "Usuario")

    user_reg = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
    user_reg.place(x=30, y=80)
    user_reg.insert(0, "Usuario")
    user_reg.bind("<FocusIn>", on_enter)
    user_reg.bind("<FocusOut>", on_leave)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

    def on_enter_cont(e):
        cont_reg.delete(0, "end")

    def on_leave_cont(e):
        name = cont_reg.get()
        if name == "":
            cont_reg.insert(0, "Contraseña")
    
     # Función para mostrar u ocultar la contraseña
    def mostrar_ocultar_registrar():
        if mostrar_contrasena_var.get():
            cont_reg.config(show='*')
        else:
            cont_reg.config(show='')
    
    # Función para mostrar u ocultar la contraseña en el campo "Confirmar Contraseña"
    def mostrar_ocultar_confirmar():
        if mostrar_confirmar_var.get():
            contfrom.config(show='*')
        else:
            contfrom.config(show='')

    cont_reg = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
    cont_reg.place(x=30, y=150)
    cont_reg.insert(0, "Contraseña")
    cont_reg.bind("<FocusIn>", on_enter_cont)
    cont_reg.bind("<FocusOut>", on_leave_cont)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

     # Crear el checkbox para mostrar/ocultar contraseña
    mostrar_contrasena_var = BooleanVar()
    mostrar_contrasena_check = Checkbutton(frame, text="Ocultar Contraseña", variable=mostrar_contrasena_var, bg="white", command=mostrar_ocultar_registrar)
    mostrar_contrasena_check.place(x=30, y=180)

    def on_enter_contfrom(e):
        contfrom.delete(0, "end")

    def on_leave_contfrom(e):
        name = contfrom.get()
        if name == "":
            contfrom.insert(0, "Confirmar Contraseña")

    contfrom = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
    contfrom.place(x=30, y=220)
    contfrom.insert(0, "Confirmar Contraseña")
    contfrom.bind("<FocusIn>", on_enter_contfrom)
    contfrom.bind("<FocusOut>", on_leave_contfrom)

    Frame(frame, width=295, height=2, bg="black").place(x=25, y=247)

    # Crear el checkbox para mostrar/ocultar "Confirmar Contraseña"
    mostrar_confirmar_var = BooleanVar()
    mostrar_confirmar_check = Checkbutton(frame, text="Ocultar Contraseña", variable=mostrar_confirmar_var, bg="white", command=mostrar_ocultar_confirmar)
    mostrar_confirmar_check.place(x=30, y=250)

    Button(frame, width=39, pady=7, text="Registrar", bg="#57a1f8", border=0, command=registrar_usuario).place(x=35, y=280)
    label = Label(frame, text="Tengo una cuenta", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
    label.place(x=90, y=340)

    sign_in = Button(frame, width=9, text="Iniciar sesión", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=ventana_registro.destroy)
    sign_in.place(x=200, y=340)

    ventana_registro.mainloop()

def mostrar_menu_principal():
    global ventana_menu
    ventana_menu = tk.Toplevel(root)
    ventana_menu.title("Menú Principal")
    ventana_menu.geometry("925x500+250+130")
    ventana_menu.configure(bg="white")
    #ventana_menu.resizable(False, False)
    
    # Maximizar la ventana
    ventana_menu.state('zoomed')
    # Quitar botones de minimizar y maximizar
    #ventana_menu.attributes('-toolwindow', True) 
 
    def actualizar_reloj():
        # Obtener la fecha y la hora actual
        ahora = datetime.now()
        fecha = ahora.strftime("%d/%m/%Y")
        hora = ahora.strftime("%I:%M:%S %p")

        # Actualizar los textos de los labels
        label_fecha.config(text=fecha)
        label_hora.config(text=hora)

        # Llamar a esta función nuevamente después de 1000 milisegundos (1 segundo)
        ventana_menu.after(1000, actualizar_reloj)

    # Crear y posicionar los labels para la fecha y la hora
    label_fecha = Label(ventana_menu, font=("Microsoft YaHei UI Light",30, "bold"), fg="#57a1f8", bg='white')
    label_fecha.place(x=ventana_menu.winfo_screenwidth() - 30, y=20, anchor='ne')

    label_hora = Label(ventana_menu, font=("Microsoft YaHei UI Light", 30, "bold"), fg="#57a1f8", bg='white')
    label_hora.place(x=ventana_menu.winfo_screenwidth() - 30, y=70, anchor='ne')

    # Llamar a la función actualizar_reloj por primera vez para iniciar el ciclo
    actualizar_reloj()

    # Cargar la imagen
    imagen_menu = PhotoImage(file="img\\Eventos.png")  # Asegúrate de que el archivo exista en la ruta especificada
    
    # Mostrar la imagen en un Label
    label_imagen_menu = Label(ventana_menu, image=imagen_menu, bg="white")
    label_imagen_menu.image = imagen_menu  # Guardar referencia a la imagen
    label_imagen_menu.pack(side="top", pady=20)

    # Crear la barra de menú
    menubar = Menu(ventana_menu, tearoff=0)
    
    
    # Crear el menú "Usuario"
    usuario_menu = Menu(menubar, tearoff=0)
    usuario_menu.add_command(label="Perfil", command=lambda: [mostrar_perfil(usuario_actual, ventana_menu, root)])
    usuario_menu.add_command(label="Cerrar sesión", command=lambda: ventana_menu.destroy())
    menubar.add_cascade(label="Usuario", menu=usuario_menu)
    
    # Crear el menú "Registrar"
    registrar_menu = Menu(menubar, tearoff=0)
    registrar_menu.add_command(label="Registrar Cliente", command=mostrar_registro_cliente)
    registrar_menu.add_command(label="Registrar Evento", command=mostrar_formulario_evento)
    menubar.add_cascade(label="Registrar", menu=registrar_menu)
    
    # Crear el menú "Transacciones"
    transacciones_menu = Menu(menubar, tearoff=0)
    transacciones_menu.add_command(label="Nueva Transacción", command=mostrar_formulario_transacciones)
    transacciones_menu.add_command(label="Historial de Transacciones", command=mostrar_historial_transacciones)
    menubar.add_cascade(label="Transacciones", menu=transacciones_menu)
    
    # Crear el menú "Consultas"
    consultas_menu = Menu(menubar, tearoff=0)
    consultas_menu.add_command(label="Consultar Cliente", command=mostrar_consultar_clientes)
    consultas_menu.add_command(label="Consultar Eventos", command=mostrar_consultar_eventos)
    menubar.add_cascade(label="Consultas", menu=consultas_menu)
    
    # Crear el menú "Registro"
    registro_menu = Menu(menubar, tearoff=0)
    registro_menu.add_command(label="Ver Registro", command=ver_registro)
    menubar.add_cascade(label="Registro", menu=registro_menu)
    
    # Crear el menú "Utilidades"
    utilidades_menu = Menu(menubar, tearoff=0)
    utilidades_menu.add_command(label="Reportes", command=solicitar_nombre_cliente)
    utilidades_menu.add_command(label="Configuraciones", command=lambda: mostrar_configuracion(usuario_actual, root, ventana_menu))
    menubar.add_cascade(label="Utilidades", menu=utilidades_menu)
    
    # Configurar la ventana para usar la barra de menú
    ventana_menu.config(menu=menubar)


# Configurar la ventana principal
root = tk.Tk()
root.title("Login")
root.geometry("925x500+250+130")
root.configure(bg="#fff")
root.resizable(False, False)
root.withdraw()  # Ocultar la ventana principal inicialmente

# Llamar a la función mostrar_bienvenida
mostrar_bienvenida()

img = PhotoImage(file="img\\login.png")
label_img = Label(root, image=img, border=0, bg="white")
label_img.image = img  # Guardar referencia a la imagen
label_img.place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text="Iniciar sesión", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
heading.place(x=60, y=5)

# Funciones para los campos de entrada
def on_enter(e):
    user.delete(0, "end")

def on_leave(e):
    name = user.get()
    if name == "":
        user.insert(0, "Usuario")

user = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
user.place(x=30, y=80)
user.insert(0, "Usuario")
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

def on_enter_cont(e):
    cont.delete(0, "end")

def on_leave_cont(e):
    name = cont.get()
    if name == "":
        cont.insert(0, "Contraseña")

# Función para mostrar u ocultar la contraseña
def mostrar_ocultar():
    if mostrar_contrasena_var.get():
        cont.config(show='*')
    else:
        cont.config(show='')

cont = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
cont.place(x=30, y=150)
cont.insert(0, "Contraseña")
cont.bind("<FocusIn>", on_enter_cont)
cont.bind("<FocusOut>", on_leave_cont)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

# Crear el checkbox para mostrar/ocultar contraseña
mostrar_contrasena_var = BooleanVar()
mostrar_contrasena_check = Checkbutton(frame, text="Ocultar Contraseña", variable=mostrar_contrasena_var, bg="white", command=mostrar_ocultar)
mostrar_contrasena_check.place(x=30, y=180)

Button(frame, width=39, pady=7, text="Iniciar sesión", bg="#57a1f8", border=0, command=verificar_credenciales).place(x=35, y=204)
label_reg = Label(frame, text="¿No tienes una cuenta?", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9))
label_reg.place(x=75, y=270)

sign_up = Button(frame, width=9, text="Registrar", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=mostrar_registro)
sign_up.place(x=215, y=270)

root.mainloop()  
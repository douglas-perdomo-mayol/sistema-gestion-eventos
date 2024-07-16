import mysql.connector
# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="eventos_db",
        port=3307  # Especifica el puerto de la base de datos
    )
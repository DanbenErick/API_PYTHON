import mysql.connector
import openpyxl

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="192.168.1.3",
    user="danben",
    password="",
    database="admision_undac"
)



# Crear un cursor
cursor = conexion.cursor()

# Abrir el archivo
libro = openpyxl.load_workbook("FORMATO_.ORDINARIO_II.xlsx")

# Acceder a la hoja de trabajo activa
hoja = libro.active

datos = []
for fila in hoja.iter_rows():
    datos.append([fila[0].value, fila[1].value])

# Mostrar la lista de listas
print(datos)

# Crear el diccionario
diccionario = []
for fila in datos:
    diccionario.append({"dni": fila[0], "codigo": fila[1]})

# Mostrar el diccionario
print(diccionario)

diccionario_terminado = diccionario[1:]

# Actualizar la base de datos
for fila in diccionario_terminado:
    sql = f"""
        UPDATE resultados
        SET CODIGO_MATRICULA = '{fila['codigo']}'
        WHERE DNI = '{fila['dni']}' AND PROCESO = 27
    """
    print("sql", sql)
    cursor.execute(sql)
    conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()
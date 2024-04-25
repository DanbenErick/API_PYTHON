import bcrypt
import pymysql.cursors

# Conexión a la base de datos (cambia los valores según tu configuración)
connection = pymysql.connect(host='192.168.1.3',
                             user='danben',
                             password='',
                             database='admision_undac',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    # Consulta para obtener todos los registros
    with connection.cursor() as cursor:
        sql = "SELECT * FROM registros"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(f"Cantidad de registros {len(data)}")
        index = 0
        for row in data:
            index = index + 1
            print(f"DNI actualizado => {row['DNI']} - Es numero {index}")
            
            # Codificar la contraseña en UTF-8
            password_utf8 = row['DNI'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password_utf8, bcrypt.gensalt(10))
            sql = f"UPDATE registros SET PASSWORD = {hashed_password} WHERE DNI = {row['DNI']}"
            print(sql)
            # Generar el hash de la contraseña

            # Actualizar el registro con el nuevo hash de contraseña
            with connection.cursor() as update_cursor:
                update_sql = "UPDATE registros SET PASSWORD = %s WHERE DNI = %s"
                update_cursor.execute(update_sql, (hashed_password.decode('utf-8'), row['DNI']))  # Decodificar el hash a UTF-8
                connection.commit()

finally:
    connection.close()

# password = 'profe-micky'
# salt = bcrypt.gensalt(10)

# hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
# print(f"{hashed_password}")
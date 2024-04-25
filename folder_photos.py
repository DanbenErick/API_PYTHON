import os

ruta_imagenes = "photos"

for archivo in os.listdir(ruta_imagenes):
    nombre_imagen, extension = os.path.splitext(archivo)
    ruta_carpeta = os.path.join(ruta_imagenes, nombre_imagen)

    print("Carpeta", ruta_carpeta, nombre_imagen, extension)

    # Crear la carpeta si no existe
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    # Mover la imagen a la carpeta
    ruta_origen = os.path.join(ruta_imagenes, archivo)
    ruta_destino = os.path.join(ruta_carpeta, archivo)
    os.rename(ruta_origen, ruta_destino)

print("Las imágenes se han movido a sus carpetas correspondientes.")

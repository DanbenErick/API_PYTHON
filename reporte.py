# import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
from reportlab.pdfgen import canvas
from datetime import datetime
import requests
import json
import os
# from dotenv import load_dotenv

# load_dotenv()
SEDE = 'TARMA'
API_NODE = 'http://143.198.105.92:3500'

def generar_pdf_service(id_proceso, inicio, fin, area, aula, fecha, sede, pdf):

    url = f"{API_NODE}/input-controls/obtener-padron-estudiantes?id_proceso={id_proceso}&inicio={inicio}&fin={fin}&area={area}&aula={aula}&fecha={fecha}&sede={sede}"
    

    print("PRINT UTILLLLLLL =====================>",url)

    

    response = requests.get(url)

    if response.status_code == 200:
        # La petición fue exitosa
        # Acceder a los datos de la respuesta
        
        datos = response.json()
        # print(datos)
    else:
        # La petición falló
        print(f"Error: {response.status_code}")


    c = canvas.Canvas(f"{pdf}.pdf", pagesize=A4)
    width, height = A4

    # print("Datao DNI", datos[0]['DNI'])

    for i, data in enumerate(datos):
        # http_imagen = f'http:192.168.1.5:3500/{data['DNI']}/{data['DNI']}.jpg'
        url_image = f"{API_NODE}/{data['DNI']}/{data['DNI']}.jpeg"
        url_image_defecto = f"{API_NODE}/defecto/defecto.jpeg"
        print("URL image => ", url_image)
        try:
            img_src = utils.ImageReader(url_image)
        except:
            img_src = utils.ImageReader(url_image_defecto)
        
        # image_no_ingreso = Image('imagenes/logo-undac.png')
        
        c.drawImage('imagenes/logo-undac.png', 30, height - 110, width=100, height=100, preserveAspectRatio=True)
        c.setFont("Helvetica-Bold", 11) #tAMAÑO DE LA FUENTE Y TIPO DE LETRA
        c.drawString(130, height - 30, "UNIVERSIDAD NACIONAL DANIEL ALCIDES CARRION")  # Añadir texto al encabezado
        c.drawString(130, height - 50, "DIRECCION DE ADMISION")
        c.drawString(130, height - 70, "EXTRAORDINARIO DE MODALIDADES 2024")
        c.drawString(130, height - 90, "PADRON DE POSTULANTES")
        c.drawString(490, height - 40, SEDE)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(470, height - 60, f"AULA: {aula}")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(490, height - 80, f"AREA {area}")
        
        
        
        #Tamaño y espaciado de las fuentes
        c.setFont("Helvetica", 10) 
        c.setFont("Helvetica-Bold", 10)
        c.drawString(33, height - 140 - ((i % 4) * 150), f"CODIGO/DNI: {data['DNI']}")  # Ajustar la posición de los datos
        c.drawString(160, height - 170 - ((i % 4) * 150), f"APELLIDO PATERNO: {data['AP_PATERNO']}")
        c.drawString(160, height - 190 - ((i % 4) * 150), f"APELLIDO MATERNO: {data['AP_MATERNO']}")
        c.drawString(160, height - 210 - ((i % 4) * 150), f"NOMBRES: {data['NOMBRES']}")
        c.setFont("Helvetica-Bold", 8) 
        c.drawString(160, height - 230 - ((i % 4) * 150), f"ESCUELA: {data['ESCUELA_COMPLETA']}")
        if(data['NOMBRE_MODALIDAD'] != None):
            c.drawString(160, height - 250 - ((i % 4) * 150), f"MODALIDAD: {data['NOMBRE_MODALIDAD']}")

        # Dibujar un rectángulo a la izquierda para la foto
        c.rect(30, height - 270 - ((i % 4) * 150), 120, 120)   

        c.drawImage(img_src, 30 + 1 , height + 1 - 270 - ((i % 4) * 150), width=119, height=119)

        # Dibujar un rectángulo para la huella digital
        c.rect(480, height - 220 - ((i % 4) * 150), 70, 70)
        c.drawString(500, height - 270 - ((i % 4) * 150), 'FIRMA')
        c.rect(480, height - 258 - ((i % 4) * 150), 70, 1, stroke=1)
        c.line(50, height - 279 - ((i % 4) * 150), width - 50, height - 279 - ((i % 4) * 150))

        # Agregar pie de página
        c.setFont("Helvetica", 8)
        c.drawString(30, 30, datetime.now().strftime("%d/%m/%Y"))  # Fecha
        c.drawCentredString(width / 2, 30, "ADMISION")  # Texto centrado "ADMISION"
        c.drawString(width - 100, 30, f"Página {i + 1}")  # Número de página

        # Crear una nueva página cada 4 resultados
        if (i + 1) % 4 == 0 and i != 0:
            c.showPage()#Persona por pagina

    # Guardar el PDF
    c.save()
    return f"{pdf}.pdf"


def generar_pdf_bloque_service(data, pdf):
    
    c = canvas.Canvas(f"{pdf}.pdf", pagesize=A4)
    width, height = A4
    # print(f"Ingreso:  {data[0]}")
    for item in data:
        url = f"{API_NODE}/input-controls/obtener-padron-estudiantes?id_proceso={item['id_proceso']}&inicio={item['inicio']}&fin={item['cantidad']}&area={item['area']}&aula={item['aula']}&fecha={item['aula']}&sede={item['sede']}"
        # url = f"http://172.16.10.11:3500/input-controls/obtener-padron-estudiantes?id_proceso={item['id_proceso']}&inicio={item['inicio']}&fin={item['cantidad']}&area={item['area']}&aula={item['aula']}&fecha={item['aula']}&sede={item['sede']}"
        print(url)
        # url = f"http://192.168.1.5:3500/input-controls/obtener-padron-estudiantes/{inicio}/{fin}/{area}"

        print("PRINT UTILLLLLLL =====================>",url)

        

        response = requests.get(url)

        if response.status_code == 200:
            # La petición fue exitosa
            # Acceder a los datos de la respuesta
            
            datos = response.json()
            # print(datos)
        else:
            # La petición falló
            print(f"Error: {response.status_code}")


        

        # print("Datao DNI", datos[0]['DNI'])

        for i, data in enumerate(datos):
            # http_imagen = f'http:192.168.1.5:3500/{data['DNI']}/{data['DNI']}.jpg'
            # url_image = f"http://172.16.10.11:3500/{data['DNI']}/{data['DNI']}.jpeg"
            # url_image_defecto = f"http://172.16.10.11:3500//defecto/defecto.jpeg"
            url_image = f"{API_NODE}/{data['DNI']}/{data['DNI']}.jpeg"
            url_image_defecto = f"{API_NODE}/defecto/defecto.jpeg"
            print("URL image => ", url_image)
            try:
                img_src = utils.ImageReader(url_image)
            except:
                img_src = utils.ImageReader(url_image_defecto)
            
            # image_no_ingreso = Image('imagenes/logo-undac.png')
            
            c.drawImage('imagenes/logo-undac.png', 30, height - 110, width=100, height=100, preserveAspectRatio=True)
            c.setFont("Helvetica-Bold", 11) #tAMAÑO DE LA FUENTE Y TIPO DE LETRA
            c.drawString(130, height - 30, "UNIVERSIDAD NACIONAL DANIEL ALCIDES CARRION")  # Añadir texto al encabezado
            c.drawString(130, height - 50, "DIRECCION DE ADMISION")
            c.drawString(130, height - 70, "EXTRAORDINARIO DE MODALIDADES 2024")
            c.drawString(130, height - 90, "PADRON DE POSTULANTES")
            c.drawString(490, height - 40, SEDE)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(470, height - 60, f"AULA: {item['aula']}")
            c.setFont("Helvetica-Bold", 11)
            c.drawString(490, height - 80, f"AREA {item['area']}")
            
            
            
            #Tamaño y espaciado de las fuentes
            c.setFont("Helvetica", 10) 
            c.setFont("Helvetica-Bold", 10)
            c.drawString(33, height - 140 - ((i % 4) * 150), f"CODIGO/DNI: {data['DNI']}")  # Ajustar la posición de los datos
            c.drawString(160, height - 170 - ((i % 4) * 150), f"APELLIDO PATERNO: {data['AP_PATERNO']}")
            c.drawString(160, height - 190 - ((i % 4) * 150), f"APELLIDO MATERNO: {data['AP_MATERNO']}")
            c.drawString(160, height - 210 - ((i % 4) * 150), f"NOMBRES: {data['NOMBRES']}")
            c.setFont("Helvetica-Bold", 8) 
            c.drawString(160, height - 230 - ((i % 4) * 150), f"ESCUELA: {data['ESCUELA_COMPLETA']}")
            if(data['NOMBRE_MODALIDAD'] != None):
                c.drawString(160, height - 250 - ((i % 4) * 150), f"MODALIDAD: {data['NOMBRE_MODALIDAD']}")

            # Dibujar un rectángulo a la izquierda para la foto
            c.rect(30, height - 270 - ((i % 4) * 150), 120, 120)   

            c.drawImage(img_src, 30 + 1 , height + 1 - 270 - ((i % 4) * 150), width=119, height=119)

            # Dibujar un rectángulo para la huella digital
            c.rect(480, height - 220 - ((i % 4) * 150), 70, 70)
            c.drawString(500, height - 270 - ((i % 4) * 150), 'FIRMA')
            c.rect(480, height - 258 - ((i % 4) * 150), 70, 1, stroke=1)
            c.line(50, height - 279 - ((i % 4) * 150), width - 50, height - 279 - ((i % 4) * 150))

            # Agregar pie de página
            c.setFont("Helvetica", 8)
            c.drawString(30, 30, datetime.now().strftime("%d/%m/%Y"))  # Fecha
            c.drawCentredString(width / 2, 30, "ADMISION")  # Texto centrado "ADMISION"
            c.drawString(width - 100, 30, f"Página {i + 1}")  # Número de página

            # Crear una nueva página cada 4 resultados
            if (i + 1) % 4 == 0 and i != 0:
                c.showPage()#Persona por pagina
            
        c.showPage()
        # Guardar el PDF
    c.save()
    return f"{pdf}.pdf"
    

    
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import requests
from reportlab.pdfgen import canvas


def generate_pdf(filename):
    # Crear un lienzo
    
    
    
    URL_API = '192.168.1.4'
    url = f'http://{URL_API}:3500/general/estudiantes/obtener-datos-estudiante-carnet'
    print("url", url)
    
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTc3MTYsInJvbCI6IkVTVFVESUFOVEUiLCJkbmkiOiI3ODc4Nzg3OCIsImlhdCI6MTcxMTg1MDc4OCwiZXhwIjoxNzExODYxNTg4fQ.7WFJqWWypSLBqyzBd6s6I_tviw7NP2t3r-UZcwG0x2c'
    
    payload = {
      "UUID" : "f6add83b-e886-11ee-b084-0242ac110002"
    }
    
    headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json"  # Si los datos están en formato JSON
    }
    
    # Realizar la solicitud GET (o POST si es necesario)
    response = requests.post(url, json=payload, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # Procesar la respuesta
        datos = response.json()  # Si la respuesta es JSON
        datos = datos[0]
        print(datos)
    else:
        print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")
    
    
    
    pdfmetrics.registerFont(TTFont('aptos', 'aptos.ttf'))
    pdfmetrics.registerFont(TTFont('aptos-bold', 'aptos-bold.ttf'))
    
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    imagen_fondo = "carnet.png"
    c.drawImage(imagen_fondo, 0, 0, width=width, height=height)

    img = f'20595791.jpeg'
    c.drawImage(img, 200, 360, width=200, height=200)

    
    AP_PATERNO = datos['AP_PATERNO']
    AP_PATERNO = datos['AP_PATERNO']
    NOMBRES = datos['NOMBRES']
    ESCUELA_COMPLETA = datos['ESCUELA_COMPLETA']
    SEDE_EXAMEN = datos['SEDE_EXAMEN']
    DNI = datos['DNI']

    # Definir el texto y su posición
    text_content = [
        ["",""],
        ["Apellido Paterno", f'{AP_PATERNO}'],
        ["Apellido Materno", f'{AP_PATERNO}'],
        ["Nombres", f'{NOMBRES}'],
        ["Mencion", f'{ESCUELA_COMPLETA}'],
        ["Sede de Examen", f'{SEDE_EXAMEN}'],
        ["Código", f'{DNI}'],
        
        # Agrega más filas según sea necesario
    ]
    
    for i in range(len(text_content)):
      print(f'Cantidad de caracteres: {text_content[i][1]} - {len( text_content[i][1])}')
      if len(text_content[i][1]) > 24:
          # Dividir la cadena en dos partes y agregar un salto de línea
          print("ingreso", text_content[i][1])
          text_content[i][1] = '\n\n'.join([text_content[i][1][j:j+24] for j in range(0, len(text_content[i][1]), 24)])

    # Crear la tabla
    table = Table(text_content)

    # Establecer el estilo de la tabla
    style = TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 20),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
                        
                        ('FONT', (0,0), (1,50), 'aptos'),
                        ('FONT', (0,0), (0,50), 'aptos-bold'),
                        ]
                       )

    table.setStyle(style)

    # Establecer el tamaño de la tabla
    table.wrapOn(c, width, height)
    table.drawOn(c, 80, 60)  # Establecer la posición de la tabla en el lienzo

    # Guardar el lienzo como PDF
    c.save()


generate_pdf('ejemplo_con_tabla.pdf')

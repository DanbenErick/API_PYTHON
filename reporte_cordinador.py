from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
import requests
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import time

from dotenv import load_dotenv
import os

load_dotenv()

api_host = os.getenv('API_NODE')


def generar_reporte_por_cordinador(proceso, dni):
    URL_API = api_host
    response = requests.get(f'http://{URL_API}:3500/input-controls/obtener-inscritos-por-cordinador?dni={dni}&proceso={proceso}')
    tiempo_documento = int(round(time.time() * 1000))
    if response.status_code == 200:
        datos = response.json()
    else:
        print(f"Error: {response.status_code}")
        # return
    data_c = [[f"Relacion de Estudiantes Inscritos por {datos[0]['CORDINADOR']} - {datos[0]['SEDE']}"]]

    # Datos para la tabla
    data = [
        ["Nro", "Postulante", "Cod Voucher", "Monto", "Fecha Voucher", "Inscrito", "Proceso"],
    ]
    suma_total = 0
    for i, element in enumerate(datos):
        suma_total = suma_total + int(element['MONTO'])
        fecha_pago_iso8601 = element['FECHA_PAGO']
        fecha_pago = datetime.fromisoformat(fecha_pago_iso8601.split('T')[0]).strftime('%Y-%m-%d')
        data.append([i + 1, element['NOMBRE_COMPLETO'], element['CODIGO'], element['MONTO'], fecha_pago, 'SI', element['NOMBRE_PROCESO']])


    data_ult = [[f"Cantidad de inscritos es {len(datos)}"], [f"El monto generado es S/ {suma_total}"]]
    # Crear documento con tamaño de página en horizontal (paisaje)
    doc = SimpleDocTemplate(f"{tiempo_documento}.pdf", pagesize=landscape(A4), leftMargin=10, rightMargin=10, topMargin=10, bottomMargin=10)

    # Obtener los estilos de muestra
    styles = getSampleStyleSheet()

    # Define un estilo personalizado para el párrafo
    # Define tus propios estilos personalizados
    custom_paragraph_style = ParagraphStyle(
        name='CustomParagraphStyle',
        fontName='Helvetica',
        fontSize=16,
        # alignment='CENTER',
        # textColor=colors.red,
    )



    # Agregar un párrafo al documento
    paragraph_text = "Este es un párrafo de ejemplo."
    paragraph = Paragraph(paragraph_text, custom_paragraph_style)

    # Calcular el ancho de la página
    width, height = landscape(A4)

    # Definir el ancho de la tabla como el 90% del ancho de la página
    table_width = width * 0.95

    # Anchos de columna en porcentajes (sumando 100%)
    column_widths = [4, 36, 10, 5, 15, 10, 20]

    # Calcular el total de los anchos de columna proporcionados
    total_column_width = sum(column_widths)

    # Calcular los anchos relativos de las columnas en función del ancho total de la tabla
    relative_column_widths = [table_width * (width_percent / total_column_width) for width_percent in column_widths]

    # Crear tabla y establecer datos con anchos de columna personalizados
    table = Table(data, colWidths=relative_column_widths)
    table_c = Table(data_c)
    table_ult = Table(data_ult)

    # Agregar la imagen de fondo
    # background_image = "background-reporte-cordinador.png"
    # image = Image(background_image, width=width, height=height)
    # image.hAlign = 'CENTER'
    # image.vAlign = 'CENTER'

    # # Agregar imagen al documento
    # doc.add(image)

    # image = Image('background-reporte-cordinador.png')

    # Crear tabla y establecer datos
    # table = Table(data)

    # Establecer estilo de la tabla
    style = TableStyle([
        # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto de encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear contenido al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para encabezado
        ('TOPPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para encabezado
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Añadir bordes a la tabla
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ])
    style_c = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para encabezado
        ('BOTTOMPADDING', (0, 0), (-1, -1), 22),  # Espaciado inferior para encabezado
        ('TOPPADDING', (0, 0), (-1, -1), 22),  # Espaciado inferior para encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear contenido al centro
        ('FONTSIZE', (0, 0), (-1, -1), 13),  # Alinear contenido al centro
        
    ])
    style_ult = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear contenido al centro
        ('FONTSIZE', (0, 0), (-1, -1), 13),  # Alinear contenido al centro
    ])


    # Cargar la imagen con ImageReader
    imagen = "background-reporte-cordinador.jpg"
    image_reader = imagen
    img_obj = Image(image_reader, width=830, height=78)

    print(width, height)

    table.setStyle(style)
    table_c.setStyle(style_c)
    table_ult.setStyle(style_ult)


    # Agregar tabla al documento
    doc.build([img_obj, table_c ,table, table_ult])
    return f"{tiempo_documento}.pdf"

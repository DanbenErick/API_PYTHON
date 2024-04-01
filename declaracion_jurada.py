from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image
import datetime
import requests
import time

def generar_declaracion_jurada(sede, proceso):
  
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        canvas.drawString(0.5 * inch, 0.45 * inch, f"FECHA DE EMISIÓN DEL DOCUMENTO: {current_date}")
        canvas.drawRightString(doc.width - 0 * inch, 0.45 * inch, "DIRECCIÓN DE ADMISIÓN")
        canvas.restoreState()

    # API_NODE = 'http://143.198.105.92:3500'
    API_NODE = 'http://172.16.10.44:3500'
    url = f"{API_NODE}/input-controls/obtener-declaraciones-juradas?sede={sede}&proceso={proceso}"

    print("PRINT UTILLLLLLL =====================>", url)

    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()
    else:
        print(f"Error: {response.status_code}")
        return

    pdf_filename = 'datos_reporte.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4, leftMargin=30, rightMargin=30, topMargin=40, bottomMargin=40)
    content = []

    for i, data in enumerate(datos):
        # image_path = f'imagenes/fotos/{codigo_postulante}.jpeg'        
        image_path = f"{API_NODE}/{data['CODIGO DE POSTULANTE']}/{data['CODIGO DE POSTULANTE']}.jpeg"
        # image_path_defecto = f"{API_NODE}/defecto/defecto.jpeg"
        foto_path_temp = image_path
        
        response = requests.get(foto_path_temp)
        current_millis = int(round(time.time() * 1000))
        temp_filename = f"fotos/temp_image_{current_millis}.jpeg"
        if response.status_code == 200:
            print("Se encontro foto ", foto_path_temp)
            # Crear un objeto Image a partir de los datos de la imagen descargada
            with open(temp_filename, "wb") as f:
                f.write(response.content)
            imagen = Image(temp_filename, width=1.5*inch, height=1.5*inch)
            
        else:
            url_temporal = f'{API_NODE}/defecto/defecto.jpeg'
            print("foto "+url_temporal)
            response = requests.get(url_temporal)
            print('Peticion foto por defecto ' + url_temporal)
            
            with open(temp_filename, "wb") as f:
                f.write(response.content)
            imagen = Image(temp_filename, width=1.5*inch, height=1.5*inch)
            print("Error al descargar la imagen desde la URL")
        
        
        # try:
        #   image = Image(image_path, width=1.5*inch, height=1.5*inch)
        # except:
        #   image_path_defecto = f"{API_NODE}/defecto/defecto.jpeg"
        #   image = Image(image_path, width=1.5*inch, height=1.5*inch)
          
        data_cabe = [['', 'CÓDIGO POSTULANTE', '3'],
                     ['', f'Nº: {data["CODIGO DE POSTULANTE"]}', ''],
                     ['', 'UNIVERSIDAD NACIONAL\nDANIEL ALCIDES CARRIÓN\nDIRECCIÓN DE ADMISIÓN', '']]
        data_cabe[0][2] = imagen
        style = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 13)
        ])

        style.add('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold')
        style.add('FONTSIZE', (1, 0), (1, 0), 18)
        style.add('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold')
        style.add('FONTSIZE', (1, 1), (1, 1), 25)
        style.add('BOTTOMPADDING', (1, 1), (1, 1), 14)

        style.add('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold')
        style.add('FONTSIZE', (1, 2), (1, 2), 14)
        style.add('LEADING', (1, 2), (1, 2), 15)

        style.add('SPAN', (2, 0), (2, 2))

        cabe = Table(data_cabe, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
        cabe.setStyle(style)

        def create_table(data):
            headers = ['', '']
            table_data = [[f'{header}:', str(value)] for header, value in data.items()]

            table = Table([headers] + table_data, colWidths=[1.5*inch, 4*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
                ('LEADING', (0, 0), (-1, -1), 6),
            ]))

            paragraph_style = ParagraphStyle(name='Normal', fontSize=13, alignment=1, spaceBefore=5, spaceAfter=12, fontName='Helvetica-Bold', underline=1, leading=10)
            ab1 = Paragraph("<u>DECLARACIÓN JURADA - CONSTANCIA INSCRIPCIÓN</u>", paragraph_style)
            paragraph_style = ParagraphStyle(name='Normal', fontSize=11, alignment=1, spaceBefore=5, spaceAfter=12, fontName='Helvetica', underline=1, leading=12)
            ab2 = Paragraph(f"Yo: {data['APELLIDOS Y NOMBRES']} con código de postulante Nº: {data['CODIGO DE POSTULANTE']} Postulante a la Carrera Profesional de: {data['FACULTAD']}. AREA: {data['ESCUELA']} al examen de {data['PROCESO']}; con los siguientes datos:", paragraph_style)
            
            paragraph_style = ParagraphStyle(name='Normal', fontSize=20, alignment=1, spaceBefore=5, spaceAfter=12, fontName='Helvetica-Bold', underline=1, leading=10)
            
            paragraph_style = ParagraphStyle(name='Normal', fontSize=15, alignment=1, spaceBefore=15, spaceAfter=12, fontName='Helvetica-Bold', underline=1)
            
            paragraph1 = Paragraph("<u>DECLARO BAJO JURAMENTO</u>", paragraph_style)
            
            paragraph_style = ParagraphStyle(name='Normal', fontSize=12, aligement=4)
            paragraph2 = Paragraph("Conocer y aceptar plenamente las disposiciones y sanciones que establece el Reglamento general de admisión. En caso de alcanzar la vacante de ingreso, me COMPROMETO a cumplir con la presentación y entrega de los documentos originales en las fechas programadas, de acuerdo a los requisitos establecidos en el reglamento general. Asimismo, acepto que, en caso de incumplimiento, mi vacante será anulada.", paragraph_style)
            paragraph_style = ParagraphStyle(name='Normal', fontSize=            12, aligement=4)
            paragraph3 = Paragraph("De conformidad con el Art. 42 de la ley 27444, DECLARO que el contenido y la documentación que presento por la presente declaración jurada son VERDADEROS y me atengo a las consecuencias y acciones legales en caso de falsedad.", paragraph_style)
            paragraph_style = ParagraphStyle(name='Normal', fontSize=12, alignment=2)
            paragraph4 = Paragraph("Cerro de Pasco, marzo de 2024", paragraph_style)
            
            return [ab1, ab2, table, paragraph1, paragraph2, paragraph3, paragraph4]

        def create_1x1_table(data):
            image_path = 'img/huella2.png'
            image = Image(image_path, width=6.4*inch, height=2.5*inch)
            table_data = [[image]]

            table = Table(table_data, colWidths=[1.7*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
                ('LEADING', (0, 0), (-1, -1), 6),
            ]))

            return [table]

        if data:
            print("pasando esto a table", data)
            content.append(cabe)
            content.extend(create_table(data))
            content.extend(create_1x1_table(data))

    doc.build(content, onFirstPage=footer, onLaterPages=footer)
    print(f"El archivo '{pdf_filename}' ha sido creado exitosamente.")

generar_declaracion_jurada('CERRO DE PASCO', 27)


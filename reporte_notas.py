from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import time
from os.path import exists
from datetime import date
import requests
from reportlab.lib.utils import ImageReader
import os

# import mysql.connector
def generar_pdf_resultados(id_proceso):
    image_no_ingreso = Image('imagenes/logo-undac.png', width=0.3*inch, height=0.3*inch)
    url_host_api = 'http://172.206.234.125:3500'
    def add_footer(canvas, doc):
        canvas.saveState()
        page_num = canvas.getPageNumber()
        text = "Página %s" % page_num
        canvas.setFont("Helvetica", 9)
        canvas.drawString(0.5 * inch, 0.3 * inch, text)

        text2 = "%s" % page_num
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(7.35 * inch, 9.9 * inch, text2)

        footer_pdf = [
            ["Elaborado por:"],
            ["Comisión de Calificación y Publicación de Resultados\ndel Primer Examen CEPRE III - 2024"],
            ["Mg. Antonio E. YANCAN CAMAHUAL"],
            ["\nFirma:"]
        ]
        footer_table = Table(footer_pdf)
        footer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, 1), (-1, 1), 0.0, colors.transparent),
        ]))
        footer_table.wrapOn(canvas, doc.width, doc.bottomMargin)
        footer_table.drawOn(canvas, 0.5 * inch, 0.5 * inch)

        footer_pdf2 = [
            ["Revisado por:"],
            ["Dirección de Admisión"],
            ["\n""\n""\n"],
        ]
        additional_table = Table(footer_pdf2, colWidths=[2.5*inch])
        additional_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        additional_table.wrapOn(canvas, doc.width, doc.bottomMargin)
        additional_table.drawOn(canvas, doc.width - 4.4 * inch, doc.bottomMargin + 1.50 * inch)

        canvas.restoreState()

        fecha_actual = date.today().strftime("%d/%m/%Y")
        canvas.setFont("Helvetica-Bold", 8)
        canvas.roundRect(doc.width - 1.5 * inch, 1.28 * inch, 1.9 * inch, 0.3 * inch, 5, stroke=1, fill=0)
        canvas.drawString(doc.width - 1.4 * inch, 1.40 * inch, f"Fecha del Proceso: {fecha_actual}")

    # conn.close()
    url = f"{url_host_api}/input-controls/obtener-resultados-ordinario/{id_proceso}"
    print("URL de datos" + url)
    resultados = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            resultados = response.json()
            print("Datos obtenidos correctamente")
            # print("Datos recibidos:", resultados)
        else:
            print("Error al obtener los datos. Código de estado:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)
    tiempo_documento = int(round(time.time() * 1000))
    doc = SimpleDocTemplate("output.pdf", pagesize=portrait(A4), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.3*inch, bottomMargin=2*inch)
    content = []


    doc.build(content, onFirstPage=add_footer, onLaterPages=add_footer)

    carrera_actual = None
    modalidad_actual = None
    registros_vistos = set()
    num = 1

    for resultado in resultados:
        codigo_carrera = resultado['COD_CARRERA']
        modalidad = resultado['ID_TIPO_MODALIDAD']
        print("Hasta aqui ingrese " + codigo_carrera + " " + modalidad)
        if codigo_carrera != carrera_actual or modalidad != modalidad_actual:
            if content:
                content.append(PageBreak())

            carrera_actual = codigo_carrera
            modalidad_actual = modalidad
            I = Image('imagenes/logo-undac.png')
            I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
            styleSheet = getSampleStyleSheet()
            I.drawWidth = 1.25*inch

            P = Paragraph(f'''
                <para align=center spaceb=3><font size=12><b>VICERRECTORADO ACADÉMICO<br/>DIRECCIÓN DE ADMISIÓN<br/>RESULTADO GENERAL DE INGRESANTES<br/>{resultado['NOMBRE_PROCESO']}</b></font></para>
            '''.encode('utf-8'), styleSheet["BodyText"])

            U = Paragraph(f'''
                <para align=center spaceb=3><font size=12><b>VICERRECTORADO ACADÉMICO</b></font></para>
            '''.encode('utf-8'), styleSheet["BodyText"])

            V = Paragraph(f'''
                <para align=center spaceb=1><font size=8><b>Código del Documento:</b></font></para>
            '''.encode('utf-8'), styleSheet["BodyText"])

            R = Paragraph(f'''
                <para align=center spaceb=1><font size=8><b>Registro de Archivo:</b></font></para>
            '''.encode('utf-8'), styleSheet["BodyText"])

            data = [
                [I, "2", "3", "4"],
                ["5", P, V, "GAC-DI-01"],
                ["9", "10", "Versión: ", "Ver. 0.1"],
                ["13", "14", "Fecha:", "16"],
                ["17", "18", R, "A15-23-03"],
                ["21", "22", "Página", ""],
            ]

            data[0][1:4] = ["UNIVERSIDAD NACIONAL DANIEL ALCIDES CARRIÓN"]
            table_4x6 = Table(data, colWidths=[1.5*inch, 3.5*inch, 1.5*inch, 1*inch])
            table_4x6.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('SPAN', (1, 0), (3, 0)),
                ('ALIGN', (1, 0), (3, 0), 'CENTER'),
            ]))

            table_4x6.setStyle(TableStyle([
                ('SPAN', (0, 0), (0, 5)),
            ]))

            table_4x6.setStyle(TableStyle([
                ('SPAN', (1, 1), (1, 5)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))

            content.append(table_4x6)

            header = [
                    ["MODALIDAD DE:", Paragraph(f"<b>{resultado['ID_TIPO_MODALIDAD']}</b>", styleSheet["BodyText"])],
                    ["FACULTAD DE:", Paragraph(f"<b>{resultado['FACULTAD']}</b>", styleSheet["BodyText"])],
                    ["PROGRAMA DE ESTUDIOS:", Paragraph(f"<b>{resultado['CARRERA']}</b>", styleSheet["BodyText"])]
                ]
            header_table = Table(header)
            header_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ]))
            content.append(header_table)
            
            print("hasta aqui llegue")
            
            data = [["", "N°", "DNI", "APELLIDOS Y NOMBRES", "PUNTAJE", "ESTADO"]]
            registros_vistos = set()
            num = 1
        else:
            data = []

        if resultado['DNI'] not in registros_vistos:
            # foto_path = f"http://172.206.234.125:3500/defecto/defecto.jpeg"
            
            if resultado['ESTADO'] == "INGRESO":
                
                # foto_path_temp = f"http://172.206.234.125:3500/{resultado['DNI']}/{resultado['DNI']}.jpeg"
                foto_path_temp = f"{url_host_api}/{resultado['DNI']}/{resultado['DNI']}.jpeg"
                print("foto "+foto_path_temp)
                
                response = requests.get(foto_path_temp)
                # Verificar si la descarga fue exitosa
                current_millis = int(round(time.time() * 1000))
                temp_filename = f"fotos/temp_image_{current_millis}.jpeg"
                if response.status_code == 200:
                    print("Se encontro foto ", foto_path_temp)
                    # Crear un objeto Image a partir de los datos de la imagen descargada
                    with open(temp_filename, "wb") as f:
                        f.write(response.content)
                    imagen = Image(temp_filename, width=1.0*inch, height=1.0*inch)
                    
                else:
                    url_temporal = f'{url_host_api}/defecto/defecto.jpeg'
                    print("foto "+url_temporal)
                    response = requests.get(url_temporal)
                    print('Peticion foto por defecto ' + url_temporal)
                    
                    with open(temp_filename, "wb") as f:
                        f.write(response.content)
                    imagen = Image(temp_filename, width=1.0*inch, height=1.0*inch)
                    print("Error al descargar la imagen desde la URL")
                
                
                image_no_ingreso = Image('imagenes/logo-undac.png', width=0.3*inch, height=0.3*inch)
                
            if resultado['ESTADO'] == "INGRESO":
                  
                data.append([
                    imagen,
                    Paragraph(f"<b><font size=15>{num}</font></b>", styleSheet["BodyText"]), 
                    Paragraph(f"<b><font size=12>{resultado['DNI']}</font></b>", styleSheet["BodyText"]), 
                    Paragraph(f"<font size=12><b>{resultado['NOMBRE_COMPLETO']}</b></font>", styleSheet["BodyText"]), 
                    Paragraph(f"<b>{resultado['PUNTAJE_TOTAL'][:-4]}</b>", styleSheet["BodyText"]), 
                    Paragraph(f"<b>{resultado['ESTADO']}</b>", styleSheet["BodyText"])
                ])
                
            else:
                # img_src.drawHeight = 0.2*inch
                # img_src.drawWidth = 0.2*inch
                data.append([
                    image_no_ingreso,
                    num, 
                    resultado['DNI'], 
                    resultado['NOMBRE_COMPLETO'], 
                    resultado['PUNTAJE_TOTAL'][:-4], 
                    resultado['ESTADO']
                ])
                
            registros_vistos.add(resultado['DNI'])
            num += 1
            
        if data:
            table = Table(data, colWidths=[1.1*inch, 0.3*inch, 0.9*inch, 3.5*inch, 0.75*inch, 0.9*inch])
            table.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            content.append(table)

    doc.build(content)
    return f"{tiempo_documento}.pdf"

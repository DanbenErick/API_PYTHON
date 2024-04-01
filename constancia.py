# from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, KeepInFrame
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
import qrcode
from reportlab.platypus import Image
from datetime import date
import time

# from fontTools import ttFont

# font = ttFont.open("Aptos.ttf")
# font.registerFont(force=True)
URL_API = '143.198.105.92'

def generar_constancias_por_proceso(proceso):

  url = f'http://{URL_API}:3500/input-controls/obtener-constancias-ingreso'
  print("url", url)
  indice_contador_contancias = 0


  # Obtiene la fecha actual
  fecha_actual = date.today()

  # Obtiene el mes como un número
  mes_numero = fecha_actual.month

  # Convierte el número del mes a un nombre
  meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
  mes_nombre = meses[mes_numero - 1]
  anio_actual = fecha_actual.year

  # Imprime el resultado
  print(f"Mes actual: {mes_nombre}")

  print(f"Mes actual: {mes_nombre} {anio_actual}")


  # Realizar la solicitud GET (o POST si es necesario)
  response = requests.get(url)

  # Verificar el estado de la respuesta
  if response.status_code == 200:
      # Procesar la respuesta
      datos = response.json()  # Si la respuesta es JSON
      # print(data)
  else:
      print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")


  tiempo_milisegundos_1 = int(time.time() * 1000)
  c = canvas.Canvas(f"{tiempo_milisegundos_1}.pdf", pagesize=A4)

  for i, data_e in enumerate(datos):
    tiempo_milisegundos = int(time.time() * 1000)
    # texto_qr = f"{data_e['DNI']}"
    texto_qr = f"https://front-undac.vercel.app/constacias-ingreso?uuid=1547a6af-8ce9-4569-8d05-7ef8040e1fdd&token=018e7d13-e7fa-7b6b-b663-4bc50e11b1e0&apellido_paterno={data_e['AP_PATERNO']}&apellido_materno={data_e['AP_MATERNO']}&nombres={data_e['NOMBRES']}&dni={data_e['DNI']}&codigo_matricula={data_e['CODIGO_MATRICULA']}&sede={data_e['SEDE_FACULTAD']}&direccion={data_e['DIRECCION_CARRERA']}&facultad={data_e['DIRECCION_CARRERA']}&proceso={data_e['NOMBRE_PROCESO']}&promedio={data_e['PROMEDIO']}"

    qr = qrcode.QRCode()
    # Establece el nivel de corrección de errores
    qr.error_correction = qrcode.constants.ERROR_CORRECT_L

    # Asigna el texto al código QR
    qr.add_data(texto_qr)

    # Crea la imagen del código QR
    img_qr = qr.make_image()

    # Guarda la imagen en un archivo
    img_qr.save(f"qrs/{tiempo_milisegundos}.png")
    
    
    # Crea un objeto `Image` con la ruta a la imagen del código QR
    # imagen_qr = Image(f"qrs/{tiempo_milisegundos}.png")

    # Establece la posición de la imagen
    

    # Agrega la imagen al lienzo
    
    
    
    # Define el tamaño A4 en píxeles
    a4_width = 2480
    a4_height = 3508
    
    # c = Canvas("", pagesize=A4)
    width, height = A4


    # Añade otros elementos al lienzo, como texto, gráficos, etc.
    x_pos = 50
    y_pos = height - 280

    pdfmetrics.registerFont(TTFont('aptos', 'aptos.ttf'))
    pdfmetrics.registerFont(TTFont('aptos-bold', 'aptos-bold.ttf'))

    

    # imagen_fondo = "constancia.jpg"
    # c.drawImage(imagen_fondo, 0, 0, width=width, height=height)
    dni = data_e['DNI']
    try:
      img = f'http://{URL_API}:3500/{dni}/{dni}.jpeg'
      c.drawImage(img, 50, 440, width=150, height=150)
      print("img", img)
    except:
      img = f'http://{URL_API}:3500/defecto/defecto.jpeg'
      c.drawImage(img, 50, 440, width=150, height=150)
      print("img", img)
          
    c.drawImage(f'qrs/{tiempo_milisegundos}.png', 50, 280, width=150, height=150)
    separador_texto = 0.35

    sample_style_sheet = getSampleStyleSheet()
    # Definir un estilo en negrita
    estilo_negrita = sample_style_sheet['BodyText']
    estilo_negrita.fontName = 'Helvetica-Bold'

    # Datos para la tabla
    data = [
        ['', ''],
        ['Apellido Paterno:', data_e['AP_PATERNO']],
        ['Apellido Materno:', data_e['AP_MATERNO']],
        ['Nombres:', data_e['NOMBRES']],
        ['DNI:', data_e['DNI']],
        ['Codigo:', data_e['CODIGO_MATRICULA']],
        ['Sede: ', data_e['SEDE_FACULTAD']],
        ['Direccion: ', data_e['DIRECCION_CARRERA']],
        ['Facultad: ', data_e['FACULTAD']],
        ['Proceso: ', data_e['NOMBRE_PROCESO']],
        ['Promedio:', data_e['PROMEDIO']],
        ['Modalidad: ', data_e['MODALIDAD']],
        ['Carrera:', data_e['CARRERA']],
        ['Semestre de inicio:', '2024 - A'],
        ['Merito:', f"{data_e['ORDEN_MERITO_1']}"],
        ['Constancia Nro:', f'{indice_contador_contancias} - 2024'],
    ]
    print("valor de tabla", data)

    ancho_max_nombre = 115
    ancho_max_edad = 210

    # Crear la tabla


    # Estilo de la tabla
    estilo_tabla = TableStyle([
        # ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),   # Alinear el texto a la izquierda
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #   ('FONT', (0, 0), (-1, 0), 'aptos'),
        ('FONTSIZE', (0, 0), (-1, -1), 13),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONT', (0,0), (1,50), 'aptos'),
        ('FONT', (0,0), (0,50), 'aptos-bold'),
      #   ('TEXTCOLOR', (0, 0), (0, -1), colors.red),
        # ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
  #   estilo_tabla.add('FONTWEIGHT', (0, 0), (0, -1), 'BOLD')  



      # Aplicar salto de línea en la segunda columna después de 22 caracteres
    for i in range(len(data)):
        print(f'Cantidad de caracteres: {data[i][1]} - {len( data[i][1])}')
        if len(data[i][1]) > 32:
            # Dividir la cadena en dos partes y agregar un salto de línea
            data[i][1] = '\n'.join([data[i][1][j:j+32] for j in range(0, len(data[i][1]), 32)])

    tabla = Table(data, colWidths=[ancho_max_nombre, ancho_max_edad])
    tabla.setStyle(estilo_tabla)
    coordenada_x = 70 + 150
    coordenada_y = 340

    alturas_filas = [altura for altura in tabla._rowHeights if altura is not None]
    altura_total = sum(alturas_filas) + 20  # Suma de las alturas de todas las filas + espacio adicional
    tabla.wrapOn(c, width, height)
    tabla.drawOn(c, coordenada_x, coordenada_y - altura_total)
    
    c.setFont("aptos", 14)
    c.drawString(70, 250, f'Se le expide la presente constancia para que proceda su matricula respectiva')
    y_pos -= inch * separador_texto
    c.setFont("aptos-bold", 14)
    c.drawString(200, 230, f'Cerro de Pasco, {mes_nombre} del {anio_actual}')
    y_pos -= inch * separador_texto
    
    c.setFont("aptos-bold", 11)
    c.drawString(40, 120, f'N° 000{indice_contador_contancias}')
    y_pos -= inch * separador_texto
    
    c.setFont("aptos-bold", 11)
    c.drawString(340, 120, f'CARGO - DIRECCION GENERAL DE ADMISION')
    y_pos -= inch * separador_texto
    
    print("Agregando pagina")
    indice_contador_contancias = indice_contador_contancias + 1
    c.showPage()

    # c.drawString(x_pos, y_pos, "Apellido Paterno: " + "apellido_paterno")
    # y_pos -= inch * separador_texto  # Desplazamiento vertical entre campos
    # c.drawString(x_pos, y_pos, "Apellido Materno: " + "apellido_materno")
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Nombres: " + "Danben Erick CRUZ BARRETO")
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "DNI: " + "73027849")
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Cogigo de Matricula: " + "1073027849")
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Sede: " + "Cerro de Pasco")
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Direccion: " + "Mi Direccion")
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Facultad: " + 'CIENCIAS EMPRESARIALEs')
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Proceso: " + 'ORDINARIO II - 2024')
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Promedio: " + 'PROMEDIO')
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "MODALIDAD: " + 'MODALIDAD')
    # y_pos -= inch * separador_texto
    # c.drawString(x_pos, y_pos, "Carrera: " + "Contabilidad")
    


  c.save()
  return f'{tiempo_milisegundos_1}.pdf'

def generar_constancia_por_estudiante(proceso, dni):
  print("Valores recibidos", proceso, dni)
  url = f'http://{URL_API}:3500/general/estudiantes/obtener-constancia-estudiante?dni={dni}&proceso={proceso}'
  print("url", url)
  indice_contador_contancias = 0

  # Obtiene la fecha actual
  fecha_actual = date.today()

  # Obtiene el mes como un número
  mes_numero = fecha_actual.month

  # Convierte el número del mes a un nombre
  meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
  mes_nombre = meses[mes_numero - 1]
  anio_actual = fecha_actual.year

  # Realizar la solicitud GET (o POST si es necesario)
  response = requests.get(url)

  # Verificar el estado de la respuesta
  if response.status_code == 200:
      
      datos = response.json()
      datos = datos[0]
      
      print("datos de la peticion: ",datos)
  else:
      print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")




  tiempo_milisegundos = int(time.time() * 1000)
  c = canvas.Canvas(f"{tiempo_milisegundos}.pdf", pagesize=A4)
  # texto_qr = f"{data_e['DNI']}"
  texto_qr = f"https://front-undac.vercel.app/constacias-ingreso?uuid=1547a6af-8ce9-4569-8d05-7ef8040e1fdd&token=018e7d13-e7fa-7b6b-b663-4bc50e11b1e0&apellido_paterno={datos['AP_PATERNO']}&apellido_materno={datos['AP_MATERNO']}&nombres={datos['NOMBRES']}&dni={datos['DNI']}&codigo_matricula={datos['CODIGO_MATRICULA']}&sede={datos['SEDE_FACULTAD']}&direccion={datos['DIRECCION_CARRERA']}&facultad={datos['DIRECCION_CARRERA']}&proceso={datos['NOMBRE_PROCESO']}&promedio={datos['PROMEDIO']}"

  qr = qrcode.QRCode()
  # Establece el nivel de corrección de errores
  qr.error_correction = qrcode.constants.ERROR_CORRECT_L

  # Asigna el texto al código QR
  qr.add_data(texto_qr)

  # Crea la imagen del código QR
  img_qr = qr.make_image()

  # Guarda la imagen en un archivo
  img_qr.save(f"qrs/{tiempo_milisegundos}.png")
  
  
  # Crea un objeto `Image` con la ruta a la imagen del código QR
  # imagen_qr = Image(f"qrs/{tiempo_milisegundos}.png")

  a4_width = 2480
  a4_height = 3508
  
  width, height = A4

  x_pos = 50
  y_pos = height - 280

  pdfmetrics.registerFont(TTFont('aptos', 'aptos.ttf'))
  pdfmetrics.registerFont(TTFont('aptos-bold', 'aptos-bold.ttf'))

  

  # imagen_fondo = "constancia.jpg"
  # c.drawImage(imagen_fondo, 0, 0, width=width, height=height)
  dni = datos['DNI']
  try:
    img = f'http://{URL_API}:3500/{dni}/{dni}.jpeg'
    c.drawImage(img, 50, 440, width=150, height=150)
    print("img", img)
  except:
    img = f'http://{URL_API}:3500/defecto/defecto.jpeg'
    c.drawImage(img, 50, 440, width=150, height=150)
    print("img", img)
        
  c.drawImage(f'qrs/{tiempo_milisegundos}.png', 50, 280, width=150, height=150)
  separador_texto = 0.35

  sample_style_sheet = getSampleStyleSheet()
  
  estilo_negrita = sample_style_sheet['BodyText']
  estilo_negrita.fontName = 'Helvetica-Bold'

  print("Datos => ", datos)
  data = [
      ['', ''],
      ['Apellido Paterno:', datos.get('AP_PATERNO', '')],
      ['Apellido Materno:', datos.get('AP_MATERNO', '')],
      ['Nombres:', datos.get('NOMBRES', '')],
      ['DNI:', datos.get('DNI', '')],
      ['Codigo:', datos.get('CODIGO_MATRICULA', '')],
      ['Sede: ', datos.get('SEDE_FACULTAD', '')],
      ['Direccion: ', datos.get('DIRECCION_CARRERA', '')],
      ['Facultad: ', datos.get('FACULTAD', '')],
      ['Proceso: ', datos.get('NOMBRE_PROCESO', '')],
      ['Promedio:', datos.get('PROMEDIO', '')],
      ['Modalidad: ', datos.get('MODALIDAD', '')],
      ['Carrera:', datos.get('CARRERA', '')],
      ['Semestre de inicio:', '2024 - A'],
      ['Merito:', f"{datos.get('ORDEN_MERITO_1', '')}"],
      ['Constancia Nro:', f"{datos.get('ID', '')} - 2024"],
  ]


  print(data)
  ancho_max_nombre = 115
  ancho_max_edad = 210

  # Crear la tabla
  estilo_tabla = TableStyle([
      ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      ('FONTSIZE', (0, 0), (-1, -1), 13),
      ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
      ('FONT', (0,0), (1,50), 'aptos'),
      ('FONT', (0,0), (0,50), 'aptos-bold'),
    
  ])
    
  for i in range(len(data)):
      print(f'Cantidad de caracteres: {data[i][1]} - {len( data[i][1])}')
      if len(data[i][1]) > 32:
          # Dividir la cadena en dos partes y agregar un salto de línea
          data[i][1] = '\n'.join([data[i][1][j:j+32] for j in range(0, len(data[i][1]), 32)])

  tabla = Table(data, colWidths=[ancho_max_nombre, ancho_max_edad])
  tabla.setStyle(estilo_tabla)
  coordenada_x = 70 + 150
  coordenada_y = 340

  alturas_filas = [altura for altura in tabla._rowHeights if altura is not None]
  altura_total = sum(alturas_filas) + 20  # Suma de las alturas de todas las filas + espacio adicional
  tabla.wrapOn(c, width, height)
  tabla.drawOn(c, coordenada_x, coordenada_y - altura_total)
  
  c.setFont("aptos", 14)
  c.drawString(70, 250, f'Se le expide la presente constancia para que proceda su matricula respectiva')
  y_pos -= inch * separador_texto
  c.setFont("aptos-bold", 14)
  c.drawString(200, 230, f'Cerro de Pasco, {mes_nombre} del {anio_actual}')
  y_pos -= inch * separador_texto
  
  c.setFont("aptos-bold", 11)
  c.drawString(40, 120, f"N° 000{datos['ID']}")
  y_pos -= inch * separador_texto
  
  c.setFont("aptos-bold", 11)
  c.drawString(340, 120, f'CARGO - DIRECCION GENERAL DE ADMISION')
  y_pos -= inch * separador_texto
  
  print("Agregando pagina")
  indice_contador_contancias = indice_contador_contancias + 1
  c.save()
  return f'{tiempo_milisegundos}.pdf'

generar_constancia_por_estudiante(26, 71223932)
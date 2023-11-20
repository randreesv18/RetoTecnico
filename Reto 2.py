import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def txt_files_to_pdf(input_folder, output_path):
    # Crear un objeto PDF con tamaño A4
    pdf_canvas = canvas.Canvas(output_path, pagesize=letter)

    # Tamaño de la página A4
    width, height = letter

    # Configurar el espacio en el que se escribirá el texto
    text_width = width - 2 * 72  # Margen izquierdo y derecho de 1 pulgada (72 puntos)
    text_height = height - 2 * 72  # Margen superior e inferior de 1 pulgada (72 puntos)

    # Posición inicial para escribir
    x, y = 72, height - 72  # Comenzar en la esquina superior izquierda

    # Iterar sobre los archivos de texto en el directorio
    for txt_file in os.listdir(input_folder):
        if txt_file.endswith('.txt'):
            txt_path = os.path.join(input_folder, txt_file)

            # Leer el contenido del archivo de texto
            with open(txt_path, 'r', encoding='utf-8') as txt_file:
                lines = txt_file.readlines()

                # Escribir el contenido en el PDF
                for line in lines:
                    # Verificar si es necesario pasar a la siguiente línea
                    if y - 12 < 72:
                        pdf_canvas.showPage()  # Pasar a una nueva página
                        y = height - 72  # Reiniciar la posición vertical

                    # Escribir la línea en el PDF
                    pdf_canvas.drawString(x, y, line.strip())

                    # Mover la posición vertical hacia abajo
                    y -= 12
    # Guardar el PDF
    pdf_canvas.save()

# Enviar correo electrónico
def sent_email(pdf_resultante):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo PDF
    with open(pdf_resultante, 'rb') as f:
        attach = MIMEApplication(f.read(),_subtype = "pdf")
        attach.add_header('Content-Disposition','attachment',filename=str('Consolidado de Boletas'))
        msg.attach(attach)

    # Establecer la conexión con el servidor SMTP y enviar el correo electrónico
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

if __name__ == '__main__':
    # Ruta de los archivos de texto
    input_directory = 'ruta donde se encuentran las boletas'
    # Ruta de salida para el archivo PDF
    output_pdf_path = 'Ruta de Salida del Archivo'
    # Establecer los parámetros del correo electrónico
    subject = 'Boletas de pago consolidadas'
    body = 'Adjunto se encuentra el archivo PDF con las boletas de pago consolidadas.'
    sender_email = 'Correo del emisor'
    sender_password = 'Usar contraseñas de aplicaciones'
    receiver_email = 'Ingrese correo del destinatario'
    pdf_resultante = 'ruta y nombre del pdf Resultante'
    try:
        # Convertir archivos de texto a un solo archivo PDF
        txt_files_to_pdf(input_directory, output_pdf_path)
        # Enviar correo
        sent_email(pdf_resultante)
    except Exception as e:
        print(f"Error: {e}")

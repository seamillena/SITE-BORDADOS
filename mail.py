import os
from dotenv import load_dotenv # type: ignore
import smtplib
from email.message import EmailMessage

load_dotenv()
destinatario = 'seamillena@gmail.com'
nome_usuario = 'Usuário Teste'

EMAIL = os.getenv('EMAIL_HOTMAIL')
SENHA = os.getenv('SENHA_HOTMAIL')

print(f"Email: {EMAIL}")
print(f"Senha: {SENHA[:4]}...")  # só pra conferir que pegou do .env

def enviar_email_confirmacao(destinatario, nome_usuario):
    msg = EmailMessage()
    msg['Subject'] = 'Confirmação de Cadastro'
    msg['From'] = EMAIL
    msg['To'] = destinatario
    msg.set_content(f'Olá {nome_usuario}, seu cadastro foi realizado com sucesso!')

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
#   
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL, SENHA)
        smtp.send_message(msg)


enviar_email_confirmacao(destinatario, nome_usuario)
print('E-mail enviado com sucesso!')

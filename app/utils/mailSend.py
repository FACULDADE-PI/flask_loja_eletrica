
from flask import render_template, request
from flask_mail import Message
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app import tokenSafe, executor, mail, app
from sys import stderr



def disparar_email_threaded(mensagem, titulo, alvo_disparo):
    msg = MIMEMultipart('alternative')
    
    msg['Subject'] = titulo
    msg['From'] = "Loja Elétrica"
    msg['To'] = alvo_disparo
    msg.attach(MIMEText(mensagem, 'html'))

    smtp_server = SMTP_SSL(app.config.get("MAIL_SERVER"), app.config.get("MAIL_PORT"))
    smtp_server.ehlo()
    smtp_server.login(app.config.get("MAIL_USERNAME"), app.config.get("MAIL_PASSWORD"))
    smtp_server.send_message(msg)
    smtp_server.close()



def send_mail_reset(email_usuario, nome_usuario):
    try:
        msg = Message("Não responda este e-mail", sender="Loja Elétrica LTDA", recipients=[email_usuario])
        generated_token = tokenSafe.dumps(email_usuario, salt=app.config.get("TOKEN_SALT"))
        data = {
            "url": "https://" + str(request.headers.get('X-Forwarded-Host', request.host)) + "/auth/reset/password/fill?token=" + generated_token,
            "userName": nome_usuario,
            "minutesExpiration": app.config.get("EXPIRATION_TOKEN", 60)
        }
        msg.html = str(render_template('emails/password_reset.html', data=data))
        executor.submit(mail.send, msg)
        return generated_token
    
    except Exception as erro:
        print(erro, file=stderr)
        return False
        

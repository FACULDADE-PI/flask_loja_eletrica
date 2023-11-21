
from flask import render_template, request
from flask_mail import Message
from app import tokenSafe, executor, mail, app
from sys import stderr



def send_mail_activation(email_usuario, nome_usuario):
    try:
        msg = Message("Não responda este e-mail", sender="Loja Elétrica LTDA", recipients=[email_usuario])
        generated_token = tokenSafe.dumps(email_usuario, salt=app.config.get("TOKEN_SALT"))
        data = {
            "url": "https://" + str(request.headers.get('X-Forwarded-Host', request.host)) + "/auth/register/confirm?token=" + generated_token,
            "userName": nome_usuario,
        }
        msg.html = str(render_template('emails/activate_account.html', data=data))
        executor.submit(mail.send, msg)
        return generated_token
    
    except Exception as erro:
        print(erro, file=stderr)
        return False
        


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
        

import random
from twilio.rest import Client

class WhatsAppService:
    def _init_(self, account_sid, auth_token, from_whatsapp_number):
        self.client = Client(account_sid, auth_token)
        self.from_whatsapp_number = from_whatsapp_number
        self.codigo_ativo = {}

    def gerar_codigo(self):
        return f"{random.randint(1000, 9999)}"

    def enviar_codigo(self, to_whatsapp_number):
        codigo = self.gerar_codigo()
        mensagem = f"Olá! Seu código de ativação é: {codigo}"

        message = self.client.messages.create(
            body=mensagem,
            from_=self.from_whatsapp_number,
            to={to_whatsapp_number}
        )
        self.codigo_ativo[to_whatsapp_number] = codigo
        print(f"Mensagem enviada! SID: {message.sid}")
        return codigo


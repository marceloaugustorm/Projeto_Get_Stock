# 📦 Projeto Get Stock - API Flask

Este projeto é uma **API em Flask** para gerenciamento de usuários e autenticação, com integração ao **Twilio WhatsApp API** para envio de códigos de validação. Faz parte do sistema **Get Stock** e inclui rotas protegidas por **JWT (JSON Web Tokens)**.

## 🚀 Tecnologias Utilizadas
- Python 3.13+
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- SQLite (default)
- Twilio API (WhatsApp)
- Docker (opcional)

## ⚙️ Configuração do Ambiente
1. Clonar o repositório:
   git clone https://github.com/marceloaugustorm/Projeto_Get_Stock.git
   cd Projeto_Get_Stock

2. Criar e ativar um ambiente virtual:
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows

3. Instalar dependências:
   pip install -r requirements.txt

4. Criar um arquivo `.env` com suas credenciais do Twilio:
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

5. Rodar a aplicação:
   python run.py

A API estará disponível em http://127.0.0.1:5000/

## 🔑 Rotas da API
### Health Check
- **GET** `/api`  
Retorna o status da API.

### Criar Usuário
- **POST** `/user`  
Body JSON:
{
  "name": "João",
  "email": "joao@email.com",
  "password": "123456",
  "cnpj": "12345678000199",
  "celular": "11999999999"
}

### Validar Código
- **POST** `/verifica/code`  
Body JSON:
{
  "cnpj": "12345678000199",
  "codigo_digitado": "1234"
}

### Login Usuário
- **POST** `/verifica`  
Body JSON:
{
  "email": "joao@email.com",
  "password": "123456"
}

### Buscar Usuário (JWT)
- **GET** `/user/<id>`  
Necessário enviar Bearer Token no Header.

### Atualizar Usuário (JWT)
- **PUT** `/user/<id>`  
Body JSON (parâmetros opcionais):
{
  "name": "Novo Nome",
  "email": "novo@email.com"
}

### Deletar Usuário (JWT)
- **DELETE** `/user/<id>`  

## 📌 Observações Importantes
- Usuários só conseguem logar após validar o código enviado via WhatsApp.
- Se estiver usando conta **trial** do Twilio, só é possível enviar mensagens para números previamente validados.
- O campo `from_` do Twilio deve ser obrigatoriamente o número `whatsapp:+14155238886` (ou outro aprovado no console).



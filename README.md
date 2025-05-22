SGHSS - Sistema de Gestão Hospitalar e Serviços de Saúde
Sobre o Projeto
O SGHSS é uma API REST desenvolvida em FastAPI para gerenciamento hospitalar, incluindo pacientes, consultas, prontuários e logs de ações no sistema. A API conta com autenticação via JWT para proteger os endpoints e garantir segurança e privacidade dos dados.

Tecnologias Utilizadas
Python 3.10+

FastAPI

SQLAlchemy

JWT (JSON Web Tokens) para autenticação

PostgreSQL (ou outro banco relacional)

Postman para testes

Como Rodar Localmente
1. Clone o repositório
git clone https://github.com/seu-usuario/sg-hss.git
cd sg-hss

3. Crie e ative o ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Instale as dependências
pip install -r requirements.txt

5. Configure variáveis de ambiente
No arquivo .env (crie se não existir), configure:
SECRET_KEY=sua_chave_secreta_super_segura
DATABASE_URL=postgresql://usuario:senha@localhost:5432/seubanco
5. Rode o servidor
uvicorn app.main:app --reload
API estará disponível em: http://localhost:8000

Autenticação JWT
Para acessar os endpoints protegidos, você precisa:

Fazer login no endpoint:

POST /usuarios/login
Com corpo JSON:

json
{
  "email": "seu@email.com",
  "senha": "suaSenha123"
}
Receberá um token JWT que deve ser enviado no cabeçalho Authorization em todas as requisições protegidas:
Authorization: Bearer seu_token_jwt_aqui
Endpoints Principais
Usuários
POST /usuarios/ — Criar usuário (requer token)

POST /usuarios/login — Login e obtenção do token

GET /usuarios/ — Listar usuários (requer token)

Pacientes
POST /pacientes/ — Criar paciente (requer token)

GET /pacientes/ — Listar pacientes (requer token)

GET /pacientes/{id} — Obter paciente por ID (requer token)

PUT /pacientes/{id} — Atualizar paciente (requer token)

DELETE /pacientes/{id} — Deletar paciente (requer token)

Consultas
POST /consultas/ — Criar consulta (requer token)

GET /consultas/ — Listar consultas (requer token)

GET /consultas/{id} — Obter consulta por ID (requer token)

DELETE /consultas/{id} — Deletar consulta (requer token)

Prontuários
CRUD similar, todos endpoints protegidos

Logs
GET /logs/ — Listar logs do sistema (requer token)

Testes com Postman
Para testar, envie o token JWT recebido no login no cabeçalho Authorization.

Teste endpoints com token válido e inválido para garantir a proteção.

Considerações sobre Segurança e LGPD
A autenticação via JWT garante que apenas usuários autorizados acessam os dados.

Logs mantêm o histórico das operações para auditoria.

Atenção à proteção de dados pessoais conforme LGPD, evitando exposição indevida.

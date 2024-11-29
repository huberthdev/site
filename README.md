# Site Servhidel - Empresa de Instalação de Energia Solar

## Descrição

> Este projeto é um site desenvolvido em Python utilizando Flask e PostgreSQL para gerenciar as solicitações de orçamento de clientes que querem instalar painéis solares em suas casas. Ele está hospedado no Heroku e atende um público geral de clientes, focado nos estados de MG, SP e GO.

## Tecnologias Utilizadas

- **Linguagem**: Python
- **Banco de Dados**: PostgreSQL
- **Hospedagem**: Heroku
- **Plataforma**: Flask

## Instalação

### Passo 1: Clone o repositório

```bash
git clone https://github.com/huberthdev/site.git
cd site

### Passo 2: Configure o ambiente virtual e instale as dependências
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### Passo 3: Execute a aplicação
python app.py

### Estrutura do Projeto
app.py: Arquivo principal da aplicação.
templates/: Arquivos HTML do projeto.
static/: Arquivos CSS, JS e imagens.
requirements.txt: Lista de dependências necessárias para o projeto.
.env: Configurações de variáveis de ambiente, como credenciais do banco de dados.

### Funcionalidades
Solicitar orçamento: [O cliente preenche Nome e Telefone (E-mail e descrição é opcional) e clica no botão Solicitar Orçamento]

Funcionalidade 2: [Breve descrição do que ela faz.]

Funcionalidade 3: [Breve descrição do que ela faz.]

### Deploy no Heroku
Baixe e instale o Heroku CLI em Heroku CLI.

**Faça login no Heroku**
heroku login

**Adicione o repositório remoto do Heroku**
heroku git:remote -a nome-do-seu-app

**Realize o deploy**
git push heroku main

### Links Importantes
Repositório no GitHub: https://github.com/huberthdev/site
Site em produção: http://www.servhidel.com.br
Nota: O domínio deste site foi adquirido no Registro.br.

### Autor
Huberth Santana da Silva
GitHub: huberthdev
E-mail: huberth.santanaup@outlook.com

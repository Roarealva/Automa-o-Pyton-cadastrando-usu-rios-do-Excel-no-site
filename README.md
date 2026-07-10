# Cadastro Automatizado de Clientes (Planilha → Site)

Projeto de estudo que demonstra como automatizar o preenchimento de um
formulário web a partir dos dados de uma planilha Excel, usando Python
e Playwright.

## O que o projeto contém

| Arquivo | O que é |
|---|---|
| `contatos.xlsx` | Planilha de exemplo com colunas `nome` e `telefone` |
| `app.py` | Site de cadastro (backend em Flask) |
| `templates/index.html` | Página HTML do site (formulário + lista de clientes) |
| `static/style.css` | Estilo visual do site |
| `automacao.py` | Script que lê a planilha e cadastra cada linha no site automaticamente |
| `requirements.txt` | Dependências Python do projeto |

## Como tudo funciona

### 1. O site (`app.py`)

É um site simples feito com **Flask** (um microframework Python para
criar sites/APIs). Ele tem três funções:

- **Cadastrar**: recebe nome e telefone pelo formulário e salva num
  arquivo `clientes.json` (funciona como um "banco de dados" simples,
  em texto).
- **Listar**: mostra todos os clientes já cadastrados numa tabela.
- **Excluir**: remove um cliente específico ou todos de uma vez.

Quando você roda `app.py`, ele sobe um servidor local. É por isso que
o site fica acessível em `http://127.0.0.1:5000` — esse endereço
("localhost") significa "este computador", ou seja, o site só roda
na sua máquina, ninguém de fora acessa.

### 2. A planilha (`contatos.xlsx`)

Tem duas colunas: `nome` e `telefone`. Vem com 5 linhas de exemplo —
você pode apagar e colocar seus próprios dados, desde que mantenha os
nomes das colunas iguais (`nome` e `telefone`), porque o script de
automação procura por esses nomes exatos.

### 3. O script de automação (`automacao.py`)

Aqui está a parte principal do aprendizado. O script:

1. Abre a planilha com a biblioteca **pandas** e lê cada linha.
2. Abre um navegador Chrome controlado pela biblioteca **Playwright**
   (você vê a janela do navegador abrindo e sendo controlada sozinha).
3. Para cada linha da planilha, ele:
   - preenche o campo "Nome"
   - preenche o campo "Telefone"
   - clica no botão "Cadastrar"
   - espera a página processar
   - passa para a próxima linha
4. No final, mostra quantos contatos foram cadastrados com sucesso.

Importante: esse script **não usa nenhum modelo de IA** — é automação
"tradicional", baseada em um roteiro fixo (sempre os mesmos campos,
sempre o mesmo botão). Esse é o tipo de tarefa que não compensa fazer
com um LLM (como o Claude) decidindo passo a passo, porque o
formulário é sempre igual — o script sozinho já resolve, sem gastar
tokens de IA a cada ação.

## Como rodar o projeto

### Pré-requisitos
- Python 3.9 ou superior instalado
- pip (gerenciador de pacotes do Python, já vem com o Python)

### Passo a passo

1. Clone o repositório e entre na pasta:
```bash
git clone <url-do-seu-repositorio>
cd <nome-da-pasta>
```

2. (Recomendado) Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale o navegador do Playwright (necessário só uma vez):
```bash
playwright install chromium
```

5. Suba o site (deixe este terminal aberto):
```bash
python app.py
```
O site vai ficar disponível em `http://127.0.0.1:5000`. Abra esse
endereço no navegador pra ver funcionando manualmente, se quiser.

6. Em **outro terminal** (com o site do passo 5 ainda rodando), rode
   a automação:
```bash
python automacao.py
```
Um navegador vai abrir sozinho e cadastrar cada linha da planilha
`contatos.xlsx` automaticamente.

7. Volte pro navegador em `http://127.0.0.1:5000` e atualize a página
   pra ver todos os clientes cadastrados na lista, com o botão de
   excluir individual ou "Excluir todos".

## Personalizando

- **Trocar os dados**: edite `contatos.xlsx` diretamente no Excel (ou
  Google Sheets, exportando como `.xlsx`), mantendo as colunas `nome`
  e `telefone`.
- **Mudar o layout do site**: edite `templates/index.html` (estrutura)
  e `static/style.css` (visual).
- **Ajustar a velocidade da automação**: no `automacao.py`, o parâmetro
  `slow_mo=300` controla a pausa (em milissegundos) entre ações — 
  aumente para ver mais devagar, diminua para rodar mais rápido.

## Observações sobre uso responsável

Este projeto foi feito como **estudo de automação com Playwright**,
usando um site próprio e controlado. Ao adaptar essa técnica para
sites de terceiros, sempre respeite os Termos de Uso do site — muitos
proíbem automação de cadastro, e sites com proteção anti-bot
(CAPTCHA, reCAPTCHA) são projetados justamente para impedir esse tipo
de ação automatizada.

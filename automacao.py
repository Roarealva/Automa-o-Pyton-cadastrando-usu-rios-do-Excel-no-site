"""
Le a planilha contatos.xlsx e cadastra cada linha (nome + telefone)
no site de cadastro, preenchendo o formulario e clicando em "Cadastrar".

Antes de rodar este script, o site (app.py) precisa estar rodando
em http://127.0.0.1:5000
"""

import sys
import time

import pandas as pd
from playwright.sync_api import sync_playwright

ARQUIVO_PLANILHA = "contatos.xlsx"
URL_SITE = "http://127.0.0.1:5000"


def carregar_contatos():
    df = pd.read_excel(ARQUIVO_PLANILHA, dtype={"telefone": str})
    df = df.dropna(subset=["nome", "telefone"])
    return df.to_dict("records")


def cadastrar_contatos(contatos):
    total = len(contatos)
    sucesso = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.goto(URL_SITE)

        for i, contato in enumerate(contatos, start=1):
            nome = str(contato["nome"]).strip()
            telefone = str(contato["telefone"]).strip()

            print(f"[{i}/{total}] Cadastrando: {nome} - {telefone}")

            try:
                page.fill("#nome", nome)
                page.fill("#telefone", telefone)
                page.click("#btn-cadastrar")
                page.wait_for_load_state("networkidle")
                sucesso += 1
                time.sleep(0.3)
            except Exception as erro:
                print(f"  Falhou ao cadastrar {nome}: {erro}")

        print(f"\nConcluido: {sucesso}/{total} contatos cadastrados.")
        time.sleep(2)
        browser.close()


if __name__ == "__main__":
    try:
        contatos = carregar_contatos()
    except FileNotFoundError:
        print(f"Arquivo '{ARQUIVO_PLANILHA}' nao encontrado.")
        sys.exit(1)

    if not contatos:
        print("Nenhum contato encontrado na planilha.")
        sys.exit(0)

    cadastrar_contatos(contatos)

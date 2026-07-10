"""
Site de cadastro de clientes (nome + WhatsApp).
Armazena os dados em um arquivo JSON local (clientes.json).
"""

import json
import os
import re

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "clientes.json")


def carregar_clientes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_clientes(clientes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=2)


def apenas_numeros(telefone):
    return re.sub(r"\D", "", telefone)


@app.route("/", methods=["GET"])
def index():
    clientes = carregar_clientes()
    return render_template("index.html", clientes=clientes)


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome", "").strip()
    telefone = apenas_numeros(request.form.get("telefone", ""))

    if not nome or not telefone:
        return redirect(url_for("index"))

    clientes = carregar_clientes()
    clientes.append({"nome": nome, "telefone": telefone})
    salvar_clientes(clientes)

    return redirect(url_for("index"))


@app.route("/excluir/<int:indice>", methods=["POST"])
def excluir(indice):
    clientes = carregar_clientes()
    if 0 <= indice < len(clientes):
        clientes.pop(indice)
        salvar_clientes(clientes)
    return redirect(url_for("index"))


@app.route("/limpar", methods=["POST"])
def limpar():
    salvar_clientes([])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)

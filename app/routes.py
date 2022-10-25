from app import app
from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash)
from app.db_functions import Chamados, session as dbsession

from app.wps import *

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        data = {
            "username": email,
            "password": password}

        res = wpslogin(data)

        if res.status_code == 200:
            result = res.json()
            contrato = result['contrato']
            cnpj = result['cnpj']
            razao_social = result['razao_social']
            session["email"] = email
            session["contrato"] = contrato
            session["cpnj"] = cnpj
            session["razao_social"] = razao_social
            return render_template('index.html', email=email, contrato=contrato, cnpj=cnpj, razao_social=razao_social)
        else:
            err = 'Dados incorretos, tente novamente'
            return render_template('login.html', erro=err)

    return render_template('login.html')


@app.route('/index')
def index():
    if "contrato" in session:
        email = session["email"]
        contrato = session["contrato"]
        cnpj = session["cpnj"]
        razao_social = session["razao_social"]
        return render_template('index.html', email=email, contrato=contrato, cnpj=cnpj, razao_social=razao_social)
    else:
        return redirect('login')


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    session.pop("contrato", None)
    session.pop("cpnj", None)
    return redirect("/")


@app.route('/novo_chamado', methods=['POST'])
def novo_chamado():
    tipo = request.form.get('tipo')
    responsavel = request.form.get('responsible')
    email = request.form.get('email')
    resumo = request.form.get('resumo')
    descricao = request.form.get('descricao')
    chamado = Chamados(tipo, responsavel, email, resumo, descricao)
    dbsession.add(chamado)
    dbsession.commit()
    id = chamado.numero
    consulta = dbsession.query(Chamados).filter(Chamados.numero == id).first()
    dbsession.close()

    return redirect('index')


@app.route('/chamados')
def chamados():
    return render_template('chamados.html')

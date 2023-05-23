from app import app

from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash, jsonify)
from app.db_functions import Chamados, Comentarios, session as dbsession
from sqlalchemy import update


from app.wps import *


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop("user", None)
    session.pop("email", None)
    session.pop("contrato", None)
    session.pop("cpnj", None)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == 'wps@wps.com' and password == '1234':
            contrato = "12345678912"
            cnpj = "22.333.333/4444-22"
            razao_social = "Empresa1"
            session["email"] = email
            session["contrato"] = contrato
            session["cpnj"] = cnpj
            session["razao_social"] = razao_social
            return redirect('chamados')
        else:
            err = 'Dados incorretos, tente novamente.'
            return render_template('login.html', erro=err)

    return render_template('login.html')

    #     data = {
    #         "username": email,
    #         "password": password}

    #     res = consultar_contrato(data)

    #     if res.status_code == 200:
    #         result = res.json()
    #         contrato = result['contrato']
    #         cnpj = result['cnpj']
    #         razao_social = result['razao_social']
    #         session["email"] = email
    #         session["contrato"] = contrato
    #         session["cpnj"] = cnpj
    #         session["razao_social"] = razao_social
    #         return redirect('chamados')
    #     else:
    #         err = 'Dados incorretos, tente novamente.'
    #         return render_template('login.html', erro=err)

    # return render_template('login.html')


@app.route('/abrir_chamado')
def abrir_chamado():
    if "contrato" in session:
        email = session["email"]
        contrato = session["contrato"]
        cnpj = session["cpnj"]
        razao_social = session["razao_social"]
        return render_template('abrir_chamado.html', email=email, contrato=contrato, cnpj=cnpj, razao_social=razao_social)
    else:
        return redirect('login')


@app.route('/atualizar_chamado', methods=['POST'])
def atualizar_chamado():
    numero = request.form.get('num')
    resumo = request.form.get('resumo')
    descricao = request.form.get('descricao')

    dbsession.query(Chamados).filter(Chamados.numero == numero).update(
        {Chamados.descricao: descricao, Chamados.resumo: resumo}, synchronize_session=False)
    dbsession.commit()

    dbsession.close()

    return redirect('chamados')


@app.route('/inclui_comentario', methods=['POST'])
def incluir_comentario():
    chamado = request.form.get('num')
    detalhes = request.form.get('detalhes')
    responsavel = request.form.get('resp')

    comentarios = Comentarios(chamado, detalhes, responsavel)
    dbsession.add(comentarios)
    dbsession.commit()

    dbsession.close()

    return redirect('chamados')

@ app.route('/incluir_comentarioexterno', methods=['POST'])
def incluir_comentarioexterno():
        
        request_data = request.get_json()

        try:
            chamado1 = request_data['id']
            detalhes = request_data['detalhes']
            responsavel = request_data['responsavel']
        except KeyError:
            retorno = {
            'return': 'json inválido',
            'status_code': '400 Bad Request'
        }
            return jsonify(retorno), 400
        else:
            consultachamado = dbsession.query(Chamados).filter(Chamados.numero == chamado1).first()
            if consultachamado == None:
                retorno = {
                    'return': 'chamado inválido',
                    'status_code': '400 Bad Request'
                }
                return jsonify(retorno), 400

            comentarios = Comentarios(chamado1, detalhes, responsavel)
            dbsession.add(comentarios)
            dbsession.commit()

            dbsession.close()

            retorno = {
                'return': 'Inserido com sucesso!',
                'status_code': '200 Ok'
            }
            return jsonify(retorno), 200




@app.route('/encerrar_chamado', methods=['GET'])
def encerrar_chamado():
    numero = request.args.get('id')

    dbsession.query(Chamados).filter(Chamados.numero == numero).update(
        {Chamados.status: 'Cancelado'}, synchronize_session=False)
    dbsession.commit()

    dbsession.close()

    return redirect('chamados')


@ app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    session.pop("contrato", None)
    session.pop("cpnj", None)
    return redirect("/")


@ app.route('/novo_chamado', methods=['POST'])
def novo_chamado():
    tipo = request.form.get('tipo')
    responsavel = request.form.get('responsible')
    email_contato = request.form.get('email')
    email = session["email"]
    contrato = session["contrato"]
    cnpj = session["cpnj"]
    razao_social = session["razao_social"]
    resumo = request.form.get('resumo')
    descricao = request.form.get('descricao')
    chamado = Chamados(tipo, responsavel, email, resumo,
                       descricao, email_contato, contrato, cnpj, razao_social)
    dbsession.add(chamado)
    dbsession.commit()
    id = chamado.numero
    consulta = dbsession.query(Chamados).filter(Chamados.numero == id).first()
    dbsession.close()

    return redirect('abrir_chamado')


@ app.route('/altera', methods=['GET'])
def altera():
    if "contrato" in session:
        contrato = session["contrato"]
        numero = request.args.get('id')
        chamado = dbsession.query(Chamados).filter(
            Chamados.numero == numero, Chamados.contrato == contrato).first()
        comentarios = dbsession.query(Comentarios).filter(
            Comentarios.chamado == numero).all()
        dbsession.close()
        return render_template('altera_chamado.html', chamado=chamado, comentarios=comentarios)
    else:
        return redirect('login')



@ app.route('/chamados')
def consultar_chamados():
    if "contrato" in session:
        contrato = session["contrato"]
        chamados = dbsession.query(Chamados).filter(
            Chamados.contrato == contrato)
        dbsession.close()
        return render_template('chamados.html', chamados=chamados)
    else:
        return redirect('login')


dbsession.close()

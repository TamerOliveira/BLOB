from app import app
from flask import render_template
from flask import request
from app.db_functions import Chamados, session


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/novo_chamado', methods=['POST'])
def novo_chamado():
    tipo = request.form.get('tipo')
    responsavel = request.form.get('responsible')
    email = request.form.get('email')
    resumo = request.form.get('resumo')
    descricao = request.form.get('descricao')
    chamado = Chamados(tipo, responsavel, email, resumo, descricao)
    session.add(chamado)
    session.commit()
    id = chamado.numero
    consulta = session.query(Chamados).filter(Chamados.numero == id).first()

    return f'''
        Chamado numero..... {consulta.numero}\n
        Data Abertura...... {consulta.data_abertura}\n
        Status............. {consulta.status}\n
        Tipo............... {consulta.tipo}\n
        Previsao........... {consulta.previsao}\n
        Responsavel........ {consulta.responsavel}\n
        Email.............. {consulta.email}\n
        Resumo............. {consulta.resumo}\n
        Descricao.......... {consulta.descricao}\n
        Solucao............ {consulta.solucao}\n
        '''

from ctypes.wintypes import PINT
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from time import strftime

engine = sqlalchemy.create_engine("sqlite:///app/database.db")
connection = engine.connect()

Base = declarative_base(engine)
session = Session()

connection.execute(""" CREATE TABLE IF NOT EXISTS CHAMADOS(
                        numero INTEGER PRIMARY KEY,
                        data_abertura VARCHAR(60) NOT NULL,
                        status VARCHAR(60) NOT NULL,
                        tipo VARCHAR(60) NOT NULL,
                        previsao VARCHAR(60) NOT NULL,
                        responsavel VARCHAR(60) NOT NULL,
                        email VARCHAR(60) NOT NULL,
                        resumo VARCHAR(150) NOT NULL,
                        descricao VARCHAR(300),
                        solucao VARCHAR(300) NOT NULL)
                        """)

#Classe da tabela de CHAMADOS
class Chamados(Base):
    __tablename__ = 'CHAMADOS'
    numero = Column('numero', Integer, primary_key=True, autoincrement=True)
    data_abertura = Column('data_abertura', String(60), nullable=False)
    status = Column('status', String(60), nullable=False)
    tipo = Column('tipo', String(60), nullable=False)
    previsao = Column('previsao', String(60), nullable=False)
    responsavel = Column('responsavel', String(60), nullable=False)
    email = Column('email', String(60), nullable=False)
    resumo = Column('resumo', String(60), nullable=False)
    descricao  = Column('descricao', String(300), nullable=True)
    solucao = Column('solucao', String(300), nullable=False)
    
    def __init__(self, tipo, responsavel, email, resumo, descricao):
        self.data_abertura = str(strftime("%d-%m-%Y"))
        self.status = 'Pendente'
        self.tipo  = tipo
        self.previsao = ''
        self.responsavel = responsavel
        self.email = email
        self.resumo = resumo
        self.descricao = descricao
        self.solucao = ''


if __name__ == '__main__':

    chamado1 = Chamados('Reparo', 'Jair', 'jair@mail.com.br', 'Peca ruim', 'Como envio?')

    session.add(chamado1)
    session.commit()
    id = chamado1.numero
    consulta = session.query(Chamados).filter(Chamados.numero==id).first()

    print(f'''
        Chamado numero..... {consulta.numero}
        Data Abertura...... {consulta.data_abertura}
        Status............. {consulta.status}
        Tipo............... {consulta.tipo}
        Previsao........... {consulta.previsao}
        Responsavel........ {consulta.responsavel}
        Email.............. {consulta.email}
        Resumo............. {consulta.resumo}
        Descricao.......... {consulta.descricao}
        Solucao............ {consulta.solucao}
        ''')
    
    # chamado1 = Chamados('Reparo', 'Jair', 'jair@mail.com.br', 'Peca ruim', 'Como envio?')
    # chamado2 = Chamados('Visita técnica', 'José', 'jose@mail.com.br', 'Cancela quebrou', 'VEnham arrumar')
    # chamado3 = Chamados('Suporte Remoto', 'Jata', 'jata@mail.com.br', 'Tela preta', 'Onde eu ligo?')

    # lista = [chamado1, chamado2, chamado3]
    # session.add_all(lista)
    # session.commit()
    # consulta = session.query(Chamados).all()

    # for i in consulta:
    #     print(f'''
    #         Data Abertura...... {i.data_abertura}
    #         Status............. {i.status}
    #         Tipo............... {i.tipo}
    #         Previsao........... {i.previsao}
    #         Responsavel........ {i.responsavel}
    #         Email.............. {i.email}
    #         Resumo............. {i.resumo}
    #         Descricao.......... {i.descricao}
    #         Solucao............ {i.solucao}
    #         ''')

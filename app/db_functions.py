from ctypes.wintypes import PINT
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from time import strftime

engine = sqlalchemy.create_engine(
    'sqlite:///app/database.db', connect_args={'check_same_thread': False})
connection = engine.connect()

Base = declarative_base(engine)
session = Session()

connection.execute(""" CREATE TABLE IF NOT EXISTS CHAMADOS(
                        numero INTEGER NOT NULL,
                        data_abertura VARCHAR(60) NOT NULL,
                        status VARCHAR(60) NOT NULL,
                        tipo VARCHAR(60) NOT NULL,
                        previsao VARCHAR(60) NOT NULL,
                        responsavel VARCHAR(120) NOT NULL,
                        email VARCHAR(60) NOT NULL,
                        email_contato VARCHAR(60) NOT NULL,
                        contrato VARCHAR(60) NOT NULL,
                        cnpj VARCHAR(20) NOT NULL,
                        razao_social VARCHAR(120) NOT NULL,
                        resumo VARCHAR(150) NOT NULL,
                        descricao VARCHAR(300),
                        solucao VARCHAR(300) NOT NULL,
                        PRIMARY KEY(numero))
                        """)

# Classe da tabela de COMENTARIOS

connection.execute(""" CREATE TABLE IF NOT EXISTS COMENTARIOS(
                        comentario INTEGER NOT NULL,
                        chamado INTEGER NOT NULL,
                        detalhes VARCHAR(300) NOT NULL,
                        responsavel VARCHAR(120) NOT NULL,
                        PRIMARY KEY (comentario),
                        FOREIGN KEY (chamado) REFERENCES CHAMADOS(numero) )
                        """)


class Chamados(Base):
    __tablename__ = 'CHAMADOS'
    numero = Column('numero', Integer, primary_key=True, autoincrement=True)
    data_abertura = Column('data_abertura', String(60), nullable=False)
    status = Column('status', String(60), nullable=False)
    tipo = Column('tipo', String(60), nullable=False)
    previsao = Column('previsao', String(60), nullable=False)
    responsavel = Column('responsavel', String(120), nullable=False)
    email = Column('email', String(60), nullable=False)
    resumo = Column('resumo', String(150), nullable=False)
    descricao = Column('descricao', String(300), nullable=True)
    solucao = Column('solucao', String(300), nullable=False)
    email_contato = Column('email_contato', String(60), nullable=False)
    contrato = Column('contrato', String(60), nullable=False)
    cnpj = Column('cnpj', String(20), nullable=False)
    razao_social = Column('razao_social', String(120), nullable=False)

    def __init__(self, tipo, responsavel, email, resumo, descricao, email_contato, contrato, cnpj, razao_social):
        self.data_abertura = str(strftime("%d-%m-%Y"))
        self.status = 'Pendente'
        self.tipo = tipo
        self.previsao = ''
        self.responsavel = responsavel
        self.email = email
        self.resumo = resumo
        self.descricao = descricao
        self.solucao = ''
        self.email_contato = email_contato
        self.contrato = contrato
        self.cnpj = cnpj
        self.razao_social = razao_social


class Comentarios(Base):
    __tablename__ = 'COMENTARIOS'
    comentario = Column('comentario', Integer,
                        primary_key=True, autoincrement=True)
    chamado = Column('chamado', Integer, ForeignKey("CHAMADOS.numero"))
    detalhes = Column('detalhes', String(300), nullable=False)
    responsavel = Column('responsavel', String(120), nullable=False)

    def __init__(self, chamado, detalhes, responsavel):
        self.chamado = chamado
        self.detalhes = detalhes
        self.responsavel = responsavel

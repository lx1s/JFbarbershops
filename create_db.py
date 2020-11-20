from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

mysql_db = {
    "drivername": "mysql+pymysql",
    "username": "root",
    "password": "root",
    "host": "localhost",
    "port": 3306,
    "database": "jfbarbearia"
}

# """Criando Tabelas do Banco de Dados"""
class Usuarios(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome =  db.Column(db.String(100))
    senha = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    adm = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, nome, senha, email, telefone):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.telefone = telefone

class Produtos(db.Model):
    id = db.Column("Cod.P",db.Integer, primary_key=True,autoincrement=True)
    nome =  db.Column(db.String(100))
    preco = db.Column(db.String(100))
    quantidade = db.Column(db.String(100))

    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade= quantidade

class agendamento(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome =  db.Column(db.String(100))
    email = db.Column(db.String(100))
    horarios = db.Column(db.String(100))

    def __init__(self, nome,email, horarios):
        self.nome = nome
        self.email = email
        self.horarios = horarios

engine = create_engine(f"{URL(**mysql_db)}")
db.Model.metadata.create_all(engine)
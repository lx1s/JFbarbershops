from flask import render_template, redirect, url_for, request, flash, session

from sqlalchemy import create_engine
from sqlalchemy.sql import text

from hashlib import sha256

from app.extensions.database import db, Usuarios, agendamento, Produtos

def init_app(app):

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    @app.route("/clientesindex", methods=["GET"])
    def pag_clientes():
        verificar = verified()
        if verificar == True:
            return render_template("/Users/pag_clientes.html")
        else:
            return redirect(url_for("index"))

    @app.route("/historia", methods=["GET"])
    def historia():
        return render_template("/Users/historia.html")

    @app.route("/servicos", methods=["GET"])
    def servicos():
        return render_template("/Users/serviços.html")
    
    @app.route("/galeria", methods=["GET"])
    def galeria():
        return render_template("/Users/galeria.html")
    @app.route("/faleconosco",methods=["GET", "POST"])
    def fale_conosco():
        return render_template("/Users/fale_Conosco.html")

    # """Login and auth"""
    @app.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            if request.form['senha'] == Usuarios.query.get['senha'] and request.form['email'] == Usuarios.query.get['email']:
                session['adm'] = 1
                print(session['adm'])
                session.permanent = True
                if session['adm'] == 1:
                    return redirect(url_for("dashboard"))
                else:
                    return redirect(url_for('pag_clientes'))
        return render_template("/Users/login.html")

    @app.route("/dashboard")
    def dashboard():
        verificar = verified()
        if verificar == False:
            agenda = agendamento.query.all()
            return render_template("/adm/dashboard.html", agenda=agenda)
        else:
            return redirect(url_for("index"))
    
    @app.route('/registrados')
    def registers():
        verificar = verified()
        if verificar == False:
            clientes = Usuarios.query.all()
            return render_template("/Adm/cadastrados.html", clientes=clientes)
        else:
            return redirect(url_for("index"))

    @app.route("/auth", methods=["POST"])
    def auth():
        statement = text("SELECT * FROM usuarios WHERE email = :email AND senha = :senha")
        email = request.form['email']
        senha = request.form['senha']
        senhahash = sha256(senha.encode()).hexdigest()
        result = engine.connect().execute(statement, email=email, senha=senhahash).fetchone()
        if result:
            if result[-1]:
                session['adm'] = 1
                return redirect(url_for("dashboard"))
            else:
                session['adm'] = 0
                return redirect(url_for('pag_clientes'))
        else:
            return redirect(url_for('adicionar_clientes'))


    @app.route('/agendar', methods=["GET","POST"])
    def cadastrarhorarios():
        verificar = verified()
        if verificar == True:
            if request.method == "POST":
                nome = request.form['nome']
                email = request.form['email']
                horarios = request.form['horarios']
                statement = text("SELECT * FROM agendamento WHERE horarios = :horarios")
                result = engine.connect().execute(statement, horarios=horarios).fetchone()
                if not result:
                    agenda = agendamento(nome, email, horarios)
                    db.session.add(agenda)
                    db.session.commit()
                    return redirect(url_for("index"))
                else:
                    flash("Esse horário ja está agendado!", category="error")
            return render_template('/Adm/horariosclientes.html')
        else:
            return redirect(url_for("index"))


    @app.route("/logout")
    def logout():
        session.pop("adm", None)
        return redirect(url_for("index"))
    

    def verified():
        if "adm" in session:
            if session['adm'] == 0:
                return True
            else:
                return False
        return False

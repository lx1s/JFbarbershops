from flask import render_template, request, url_for, redirect, flash, session

from hashlib import sha256

from sqlalchemy.sql import text
from sqlalchemy import create_engine

from app.extensions.database import Usuarios, Produtos, agendamento, db

def init_app(app):

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])


    @app.route('/registrados', methods=["GET"])
    def registrados():
        clientes = Usuarios.query.all()
        return render_template('/Adm/cadastrados.html', clientes=clientes)

    @app.route('/produtos_registrados', methods=["GET"])
    def prod_cadastrados():
        verificar = verify()
        if verificar == True:
            produtos = Produtos.query.all()
            return render_template('/Adm/produtos_cadastrados.html', produtos=produtos)
        else:
            return redirect(url_for("index"))

        # """Página de Clientes"""
    @app.route('/cadastrar', methods=["GET", "POST"])
    def adicionar_clientes():
        if request.method == "POST":
            passw = request.form['senha']
            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']
            hashpass = sha256(passw.encode()).hexdigest()
            statement = text('SELECT * FROM usuarios WHERE email = :email')
            statement2 = text("SELECT * FROM usuarios WHERE telefone = :telefone")
            result = engine.connect().execute(statement, email=email).fetchone()
            result2 = engine.connect().execute(statement2, telefone=telefone).fetchone()
            if result or result2:
                flash("Email ou Telefone ja cadastrado!", category="error")
                return redirect(url_for('adicionar_clientes'))
            else:
                clientes = Usuarios(nome,hashpass, email, telefone)
                db.session.add(clientes)
                db.session.commit()
                return redirect(url_for('login'))
        return render_template('/Adm/cadastrar.html')

    @app.route('/deletarClientes/<int:id>')
    def deletar_clientes(id):
        verificar = verify()
        if verificar == True:
            clientes = Usuarios.query.get(id)
            db.session.delete(clientes)
            db.session.commit()
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("index"))

    @app.route('/editarClientes/<int:id>', methods=["GET","POST"])
    def editar_clientes(id):
        verificar = verify()
        if verificar == True:
            clientes =  Usuarios.query.get(id)
            if request.method == "POST":
                passw = request.form['senha']
                clientes.nome = request.form['nome']
                clientes.senha = sha256(passw.encode()).hexdigest()
                clientes.email = request.form['email']
                clientes.telefone = request.form['telefone']
                db.session.commit()
                return redirect(url_for('pag_adm'))
            return render_template('/Adm/editar_cadastro.html', clientes=clientes)
        else:
            return redirect(url_for("index"))

    # Cadastramento e edição de horarios
    @app.route('/agendarhorario', methods=["GET", "POST"])
    def cadastrahorarios():
        verificar = verify()
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
                    return redirect(url_for("pag_clientes"))
                else:
                    flash("Esse horário ja está agendado!", category="error")
            return render_template('/Adm/horarios.html')
        else:
            return redirect(url_for("index"))

    @app.route('/horarios', methods=["GET"])
    def horarios():
        verificar = verify()

        if verificar == True:
            agenda = agendamento.query.all()
            return render_template("/Adm/horarioscadastrados.html", agenda=agenda)
        else:
            return redirect(url_for("index"))

    @app.route('/editarhorarios/<int:id>', methods=["GET", "POST"])
    def editar_horarios(id):
        verificar = verify()
        if verificar == True:
            agenda =  agendamento.query.get(id)
            if request.method == "POST":
                agenda.nome = request.form['nome']
                agenda.email = request.form['email']
                agenda.horarios = request.form['horarios']
                db.session.commit()
                return redirect(url_for('dashboard'))
            return render_template('/Adm/editarhorarios.html', agenda=agenda)
        else:
            return redirect(url_for("index"))

    @app.route('/deletarhorarios/<int:id>')
    def deleta_horarios(id):
        verificar = verify()
        if verificar == True:
            deletar = agendamento.query.get(id)
            db.session.delete(deletar)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for("index"))

        # """Página de Produtos"""
    @app.route('/cadastro_de_produtos', methods=["GET", "POST"])
    def cadastro_de_produtos():
        verificar = verify()

        if verificar == True:
            if request.method == "POST":
                nome = request.form['nome']
                preco = request.form['preco']
                quantidade = request.form['quantidade']
                statement = text("SELECT * FROM produtos WHERE nome = :nome")
                result = engine.connect().execute(statement, nome=nome).fetchone()
                if not result:
                    produtos = Produtos(nome, preco, quantidade)
                    db.session.add(produtos)
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    flash("Esse produto já foi cadastrado!", category="error")
            return render_template('/Adm/cadastrar_produtos.html')
        else:
            return redirect(url_for("index"))

    @app.route("/cadastrar_produtos", methods=["POST"])
    def cadastrarProdutos():
        verificar = verify()
        if verificar == True:
            nome = request.form['nome']
            preco = request.form['preco']
            quantidade = request.form['quantidade']
            statement = text("SELECT * FROM produtos WHERE nome = :nome")
            result = engine.connect().execute(statement, nome=nome).fetchone()
            if not result:
                produtos = Produtos(nome, preco, quantidade)
                db.session.add(produtos)
                db.session.commit()
                return redirect(url_for('pag_adm'))
            else:
                flash("Esse produto já foi cadastrado!", category="error")
        else:
            return redirect(url_for("index"))
        return render_template('/Adm/cadastrar_produtos.html')

    @app.route('/editarProdutos/<int:id>', methods=["GET", "POST"])
    def editar_produtos(id):
        verificar = verify()

        if verificar == True:
            produtos = Produtos.query.get(id)
            if request.method == "POST":
                produtos.nome = request.form['nome']
                produtos.preco = request.form['preco']
                db.session.commit()
                return redirect(url_for('prod_cadastrados'))
            return render_template('/Adm/editar_produtos.html', produtos=produtos)
        else:
            return redirect(url_for("index"))

    @app.route('/deletarProdutos/<int:id>')
    def deletar_produtos(id):
        verificar = verify()
        if verificar == True:
            produtos = Produtos.query.get(id)
            db.session.delete(produtos)
            db.session.commit()
            return redirect(url_for("pag_adm"))
        else:
            return redirect(url_for("index"))


def verify():
    if "adm" in session:
        if session['adm'] == 1:
            return True
        else:
            return False
    return False
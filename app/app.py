from flask import Flask

from app.extensions import database
from app.extensions import bootstrap
from app.views import adm, users, index

def create_app():

    app = Flask(__name__)

    app.secret_key = "000"

    bootstrap.init_app(app)
    database.init_app(app)
    index.init_app(app)
    users.init_app(app)
    adm.init_app(app)

    return app

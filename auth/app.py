from os import pipe
from flask import Flask
from dotenv import load_dotenv
from auth.utils.pipeline import Pipeline
from auth.database.criar import criar_tabelas
from auth.controllers.usuario import ControllerUsuario

from auth.validators.usuario import ValidatorUsuario


# Inicialização de aplicação
load_dotenv("auth/config/.env")
application = Flask(__name__)
criar_tabelas()


@application.route("/usuario/novo", methods=["POST"])
def home():
    return Pipeline.run(
        ValidatorUsuario.criacao,
        ControllerUsuario.criar
    )

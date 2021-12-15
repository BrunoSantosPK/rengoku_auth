from os import pipe
from flask import Flask
from dotenv import load_dotenv
from auth.utils.pipeline import Pipeline
from auth.database.criar import criar_tabelas

from auth.validators.usuario import ValidatorUsuario
from auth.validators.autenticacao import ValidatorAutenticacao

from auth.controllers.usuario import ControllerUsuario
from auth.controllers.autenticacao import ControllerAutenticacao


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


@application.route("/usuario/login", methods=["POST"])
def login():
    return Pipeline.run(
        ValidatorUsuario.login,
        ControllerUsuario.login
    )


@application.route("/usuario/autenticado", methods=["GET"])
def autenticado():
    return Pipeline.run(
        ValidatorAutenticacao.validar,
        ControllerAutenticacao.validar
    )


@application.route("/usuario/alterar/senha", methods=["PUT"])
def alterar_senha():
    return Pipeline.run(
        ValidatorAutenticacao.validar,
        ControllerAutenticacao.validar,
        ValidatorUsuario.alterar_senha,
        ControllerUsuario.alterar_senha
    )

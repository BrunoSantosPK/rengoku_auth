import json
from flask import request
from auth.utils.response import Response
from validator import validate, rules as R


class ValidatorUsuario:

    @staticmethod
    def criacao() -> Response:
        req: dict = json.loads(request.data)
        req["email"] = "" if "email" not in req.keys() else req["email"]
        res = Response()

        regras = {
            "email": [R.Required, R.Mail],
            "nome": [R.Required, R.Min(5)],
            "senha": [R.Required, R.Min(8)],
            "senha_repeticao": [R.Required, R.Min(8)]
        }

        valido, _, erros = validate(req, regras, return_info=True)
        if not valido:
            res.set_status(400)
            res.set_attr("log", erros)
        
        return res

    @staticmethod
    def login() -> Response:
        res = Response()
        req: dict = json.loads(request.data)
        req["email"] = "" if "email" not in req.keys() else req["email"]

        regras = {
            "email": [R.Required, R.Mail],
            "senha": [R.Required, R.Min(8)]
        }

        valido, _, erros = validate(req, regras, return_info=True)
        if not valido:
            res.set_status(400)
            res.set_attr("log", erros)
        
        return res

    @staticmethod
    def alterar_senha() -> Response:
        res = Response()
        req: dict = json.loads(request.data)
        req["email"] = "" if "email" not in req.keys() else req["email"]

        regras = {
            "email": [R.Required, R.Mail],
            "senha_antiga": [R.Required, R.Min(8)],
            "senha_nova": [R.Required, R.Min(8)],
            "senha_nova_repeticao": [R.Required, R.Min(8)]
        }

        valido, _, erros = validate(req, regras, return_info=True)
        if not valido:
            res.set_status(400)
            res.set_attr("log", erros)
        
        return res

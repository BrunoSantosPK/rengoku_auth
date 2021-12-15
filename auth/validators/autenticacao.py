import json
from flask import request
from auth.utils.response import Response
from validator import validate, rules as R


class ValidatorAutenticacao:

    @staticmethod
    def validar() -> Response:
        req: dict = request.headers
        res = Response()

        regras = {
            "authorization": [R.Required],
            "id": [R.Required]
        }

        valido, _, erros = validate(req, regras, return_info=True)
        if not valido:
            res.set_status(400)
            res.set_attr("log", erros)
        
        return res

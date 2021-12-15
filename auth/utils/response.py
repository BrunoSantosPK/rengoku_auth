import json


class Response:

    def __init__(self):
        self.__body = {
            "statusCode": 200,
            "log": ""
        }

    def set_status(self, valor: int):
        '''
        Define o status para response. Alguns padrões internos:
        200: sucesso
        400: requisição inválida
        401: usuário não autorizado
        444: regra de negócio não atendida
        445: erro de código
        '''
        self.__body["statusCode"] = valor
    
    def set_attr(self, attr: str, valor: int or float or str or bool):
        self.__body[attr] = valor

    def get_status(self) -> int:
        return self.__body["statusCode"]

    def get_json(self) -> str:
        return json.dumps(self.__body)

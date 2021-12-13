import os
import jwt
from typing import Tuple
from datetime import datetime, timedelta


class ControllerAutenticacao:
    
    @staticmethod
    def gerar_jwt(id: int) -> Tuple[bool, str]:
        sucesso, token = True, ""
        chave = os.getenv("SECRET")
        payload = {
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "sub": id
        }

        try:
            token = str(jwt.encode(payload, chave, algorithm="HS256"))
        except Exception as e:
            sucesso = False
            token = str(e)
        finally:
            return sucesso, token

    @staticmethod
    def validar_jwt(token: str, id: int) -> Tuple[bool, str]:
        sucesso, msg = True, ""
        chave = os.getenv("SECRET")

        try:
            payload = jwt.decode(token, chave, algorithms="HS256")
            if payload["sub"] != id:
                sucesso = False
                msg = "Token não relacionado ao usuário."

        except jwt.ExpiredSignatureError:
            sucesso = False
            msg = "Validade do token expirada."

        except jwt.InvalidTokenError:
            sucesso = False
            msg = "Formato do token inválido."

        except BaseException as e:
            sucesso = False
            msg = str(e)

        finally:
            return sucesso, msg

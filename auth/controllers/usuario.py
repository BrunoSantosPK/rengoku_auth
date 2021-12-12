import json
from flask import request
from datetime import datetime
from auth.models.tabelas import Usuarios
from auth.utils.response import Response
from auth.database.conexao import get_session


class ControllerUsuario:

    @staticmethod
    def criar() -> Response:
        # Recupera corpo da requisição e inicia variáveis de controle
        body = json.loads(request.data)
        session = get_session()
        res = Response()
        valido = True

        try:
            # Verificar se senhas são iguais
            if body["senha"] != body["senha_repeticao"]:
                valido = False
                res.set_status(444)
                res.set_attr("log", "Senhas não correspondentes.")

            # Verificar se o email já está cadastrado
            if valido:
                q = session.query(Usuarios).filter_by(email=body["email"])
                if len(q.all()) != 0:
                    valido = False
                    res.set_status(444)
                    res.set_attr("log", "O e-mail já está cadastrado.")

            # Registra informação no banco
            if valido:
                session.add(Usuarios(
                    nome=body["nome"],
                    email=body["email"],
                    senha=ControllerUsuario.codificar(body["senha"]),
                    data_criacao=datetime.utcnow().isoformat()
                ))
                session.commit()
            
        except BaseException as e:
            session.rollback()
            res.set_attr("log", str(e))

        finally:
            session.close()

        return res

    @staticmethod
    def alterar_senha() -> Response:
        pass

    @staticmethod
    def recuperar_senha() -> Response:
        pass

    @staticmethod
    def codificar(senha) -> str:
        return senha

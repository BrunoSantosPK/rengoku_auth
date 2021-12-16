import os
import json
import hashlib
import binascii
from flask import request
from datetime import datetime
from auth.models.tabelas import Usuarios
from auth.utils.response import Response
from auth.database.conexao import get_session
from auth.controllers.autenticacao import ControllerAutenticacao


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
            session.begin()
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
    def login() -> Response:
        # Recupera corpo da requisição e inicia variáveis de controle
        body = json.loads(request.data)
        session = get_session()
        res = Response()
        
        try:
            session.begin()
            email = body["email"]
            senha = ControllerUsuario.codificar(body["senha"])

            q = session.query(Usuarios).filter_by(
                email=email,
                senha=senha
            ).all()

            if len(q) == 1:
                sucesso, token = ControllerAutenticacao.gerar_jwt(q[0].id)
                if sucesso:
                    data = {
                        "id": q[0].id,
                        "email": q[0].email,
                        "nome": q[0].nome,
                        "token": token
                    }
                    res.set_attr("data", data)
                else:
                    res.set_status(445)
                    res.set_attr("log", "Falha na geração do JWT.")
            else:
                res.set_status(444)
                res.set_attr("log", "Usuário ou senha incorretos.")

        except BaseException as e:
            session.rollback()
            res.set_status(445)
            res.set_attr("log", str(e))

        finally:
            session.close()

        return res

    @staticmethod
    def alterar_senha() -> Response:
        # Recupera corpo da requisição e inicia variáveis de controle
        body = json.loads(request.data)
        session = get_session()
        res = Response()

        try:
            # Verifica senha atual informada
            session.begin()
            senha = ControllerUsuario.codificar(body["senha_nova"])
            q = session.query(Usuarios).filter_by(
                email=body["email"],
                senha=ControllerUsuario.codificar(body["senha_antiga"])
            ).all()

            # Sequência de validações de regras de negócio
            if len(q) != 1:
                res.set_status(444)
                res.set_attr("log", "A senha atual não está correta.")

            elif body["senha_antiga"] == body["senha_nova"]:
                res.set_status(444)
                res.set_attr("log", "A nova senha não deve ser igual a senha antiga.")

            elif body["senha_nova"] != body["senha_nova_repeticao"]:
                res.set_status(444)
                res.set_attr("log", "As novas senhas não são iguais.")

            else:
                # Altera a senha no banco de dados
                session.query(Usuarios).filter(
                    Usuarios.id == q[0].id
                ).update({"senha": senha})
                session.commit()
        
        except BaseException as e:
            session.rollback()
            res.set_status(445)
            res.set_attr("log", str(e))
        
        finally:
            session.close()

        return res

    @staticmethod
    def recuperar_senha() -> Response:
        pass

    @staticmethod
    def codificar(senha: str) -> str:
        token = os.getenv("TOKEN")
        pw = (senha + token).encode("utf-8")
        hash = hashlib.pbkdf2_hmac("sha256", pw, token.encode("utf-8"), 100000)
        hash = binascii.hexlify(hash).decode("ascii")
        return hash

import json
import requests


def get_novo_usuario() -> dict:
    return {
        "email": "teste@teste.com",
        "nome": "Usuário Teste",
        "senha": "senha_generica",
        "senha_repeticao": "senha_generica"
    }


def test_requisicao_errada():
    url = "http://localhost:3636/usuario/novo"
    casos = ["", "senha", "nome", "email"]
    status = 400

    for caso in casos:
        body = get_novo_usuario()
        if caso in body.keys():
            body[caso] = "abc"
        else:
            body = {}

        r = requests.post(url, json=body)
        st = r.json()["statusCode"]
        status = st if st != 400 else status

    assert status == 400


def test_senha_fraca():
    pass


def test_email_invalido():
    pass


def test_nome_invalido():
    pass


def test_criar_usuario():
    url = "http://localhost:3636/usuario/novo"
    r = requests.post(url, json=get_novo_usuario())
    assert r.json()["log"] == ""


def test_usuario_existente():
    url = "http://localhost:3636/usuario/novo"
    r = requests.post(url, json=get_novo_usuario())
    assert r.json()["log"] == "O e-mail já está cadastrado."


def test_deletar_usuario():
    pass

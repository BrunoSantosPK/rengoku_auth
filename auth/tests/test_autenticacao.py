import requests


def test_login():
    url = "http://localhost:3636/usuario/login"
    body = {
        "email": "teste@teste.com",
        "senha": "senha_generica",
    }
    r = requests.post(url, json=body)
    assert r.json()["statusCode"] == 200


def test_corpo_erado():
    url = "http://localhost:3636/usuario/login"
    r = requests.post(url, json={})
    assert r.json()["statusCode"] == 400


def test_jwt_invalido():
    pass

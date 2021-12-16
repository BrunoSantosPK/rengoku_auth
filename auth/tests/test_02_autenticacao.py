import json
import requests


def get_usuario():
    return {"email": "teste@teste.com", "senha": "senha_generica"}


def test_login():
    url = "http://localhost:3636/usuario/login"
    r = requests.post(url, json=get_usuario())
    assert r.json()["statusCode"] == 200


def test_corpo_erado():
    url = "http://localhost:3636/usuario/login"
    r = requests.post(url, json={})
    assert r.json()["statusCode"] == 400


def test_autenticado():
    url = "http://localhost:3636/usuario/login"
    r = requests.post(url, json=get_usuario()).json()

    header = {
        "authorization": r["data"]["token"],
        "id": str(r["data"]["id"])
    }

    url = "http://localhost:3636/usuario/autenticado"
    r = requests.get(url, headers=header)
    assert r.json()["statusCode"] == 200


def test_sem_header():
    url = "http://localhost:3636/usuario/autenticado"
    r = requests.get(url, headers={})
    assert r.json()["statusCode"] == 400


def test_jwt_invalido():
    url = "http://localhost:3636/usuario/autenticado"
    header = {"authorization": "sfasdf", "id": "4"}
    r = requests.get(url, headers=header)
    assert r.json()["statusCode"] == 401

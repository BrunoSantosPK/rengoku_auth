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
    r = requests.post(url, json={})
    assert r.json()["statusCode"] == 400


def test_senha_fraca():
    url = "http://localhost:3636/usuario/novo"
    body = get_novo_usuario()
    body["senha"] = "abc"

    r = requests.post(url, json=body)
    assert r.json()["statusCode"] == 400


def test_email_invalido():
    url = "http://localhost:3636/usuario/novo"
    body = get_novo_usuario()
    body["email"] = "email.com"
    
    r = requests.post(url, json=body)
    assert r.json()["statusCode"] == 400


def test_nome_invalido():
    url = "http://localhost:3636/usuario/novo"
    body = get_novo_usuario()
    body["nome"] = "abc"
    
    r = requests.post(url, json=body)
    assert r.json()["statusCode"] == 400


def test_senhas_diferentes():
    url = "http://localhost:3636/usuario/novo"
    body = get_novo_usuario()
    body["senha"] = "senha_valida"
    body["senha_repeticao"] = "senha_diferente"
    
    r = requests.post(url, json=body)
    assert r.json()["statusCode"] == 444


def test_criar_usuario():
    url = "http://localhost:3636/usuario/novo"
    r = requests.post(url, json=get_novo_usuario())
    assert r.json()["statusCode"] == 200


def test_usuario_existente():
    url = "http://localhost:3636/usuario/novo"
    r = requests.post(url, json=get_novo_usuario())
    assert r.json()["statusCode"] == 444

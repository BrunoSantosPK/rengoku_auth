import requests


def get_body():
    return {
        "email": "teste@teste.com",
        "senha_antiga": "senha_generica",
        "senha_nova": "nova_senha",
        "senha_nova_repeticao": "nova_senha"
    }


def get_header():
    body = {"email": "teste@teste.com", "senha": "senha_generica"}
    url = "http://localhost:3636/usuario/login"
    r = requests.post(url, json=body).json()

    return {
        "authorization": r["data"]["token"],
        "id": str(r["data"]["id"])
    }


def test_corpo_invalido():
    url = "http://localhost:3636/usuario/alterar/senha"
    r = requests.put(url, json={}, headers=get_header())
    assert r.json()["statusCode"] == 400


def test_senha_antiga_invalida():
    url = "http://localhost:3636/usuario/alterar/senha"
    body = get_body()
    body["senha_antiga"] = "senha_errada"

    r = requests.put(url, json=body, headers=get_header())
    assert r.json()["statusCode"] == 444


def test_senha_nova_igual_antiga():
    url = "http://localhost:3636/usuario/alterar/senha"
    body = get_body()
    body["senha_nova"] = "senha_generica"

    r = requests.put(url, json=body, headers=get_header())
    assert r.json()["statusCode"] == 444


def test_senhas_novas_diferentes():
    url = "http://localhost:3636/usuario/alterar/senha"
    body = get_body()
    body["senha_nova"] = "senha_diferente"

    r = requests.put(url, json=body, headers=get_header())
    assert r.json()["statusCode"] == 444


def test_alterar_senha():
    url = "http://localhost:3636/usuario/alterar/senha"
    body = get_body()

    r = requests.put(url, json=body, headers=get_header())
    assert r.json()["statusCode"] == 200

import os
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine


def get_engine() -> Engine:
    usuario = os.getenv("USUARIO_DB")
    senha = os.getenv("SENHA_DB")
    banco = os.getenv("NOME_DB")
    host = os.getenv("HOST_DB")
    return create_engine(f"postgresql://{usuario}:{senha}@{host}/{banco}")


def get_session() -> Session:
    engine = get_engine()
    return Session(engine)

from auth.models.tabelas import Base
from auth.database.conexao import get_engine


def criar_tabelas():
    Base.metadata.create_all(get_engine())

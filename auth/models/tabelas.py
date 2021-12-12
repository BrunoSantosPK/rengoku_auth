from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class Usuarios(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "adm"}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    data_criacao = Column(DateTime)

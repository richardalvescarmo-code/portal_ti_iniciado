import re
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    usuario = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )

    senha_hash = db.Column(
        db.String(255),
        nullable=False
    )

    perfil = db.Column(
        db.String(30),
        nullable=False,
        default="usuario"
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    # Preferencias de aparencia do usuario.
    # Os valores possiveis sao validados na rota, nunca aqui,
    # porque o banco nao deve ser a unica linha de defesa.
    tema = db.Column(
        db.String(10),
        nullable=False,
        default="claro"
    )

    cor_primaria = db.Column(
        db.String(20),
        nullable=False,
        default="azul"
    )

    ultimo_login = db.Column(
        db.DateTime,
        nullable=True
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    @staticmethod
    def validar_senha(senha: str):
        if not senha:
            return False, "Informe uma senha."

        if len(senha) < 8:
            return (
                False,
                "A senha deve ter pelo menos 8 caracteres."
            )

        if not re.search(r"[A-Z]", senha):
            return (
                False,
                "A senha deve conter pelo menos uma letra maiúscula."
            )

        if not re.search(r"[a-z]", senha):
            return (
                False,
                "A senha deve conter pelo menos uma letra minúscula."
            )

        if not re.search(r"\d", senha):
            return (
                False,
                "A senha deve conter pelo menos um número."
            )

        if not re.search(r"[^A-Za-z0-9]", senha):
            return (
                False,
                "A senha deve conter pelo menos um caractere especial."
            )

        return True, None

    def definir_senha(self, senha: str) -> None:
        senha_valida, mensagem = self.validar_senha(
            senha
        )

        if not senha_valida:
            raise ValueError(
                mensagem
            )

        self.senha_hash = generate_password_hash(
            senha
        )

    def verificar_senha(self, senha: str) -> bool:
        if not senha:
            return False

        return check_password_hash(
            self.senha_hash,
            senha
        )

    @property
    def is_active(self) -> bool:
        return self.ativo

    def registrar_login(self) -> None:
        self.ultimo_login = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Usuario {self.usuario}>"
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

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

    def definir_senha(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha: str) -> bool:
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
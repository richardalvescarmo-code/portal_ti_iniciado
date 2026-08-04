from datetime import datetime

from extensions import db


class Ferramenta(db.Model):
    __tablename__ = "ferramentas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    categoria = db.Column(
        db.String(80),
        nullable=True
    )

    descricao = db.Column(
        db.String(255),
        nullable=True
    )

    url_acesso = db.Column(
        db.String(500),
        nullable=False
    )

    icone = db.Column(
        db.String(80),
        nullable=False,
        default="bi-tools"
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
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

    def __repr__(self):
        return f"<Ferramenta {self.nome}>"
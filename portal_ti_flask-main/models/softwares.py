from datetime import datetime

from extensions import db


class Software(db.Model):
    __tablename__ = "softwares"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    descricao = db.Column(
        db.String(255),
        nullable=True
    )

    categoria = db.Column(
        db.String(80),
        nullable=True
    )

    url_download = db.Column(
        db.String(500),
        nullable=True
    )

    arquivo_nome = db.Column(
        db.String(255),
        nullable=True
    )

    arquivo_original = db.Column(
        db.String(255),
        nullable=True
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
        return f"<Software {self.nome}>"
from datetime import datetime

from extensions import db


class Procedimento(db.Model):
    __tablename__ = "procedimentos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(150),
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

    conteudo = db.Column(
        db.Text,
        nullable=False
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
        return f"<Procedimento {self.titulo}>"
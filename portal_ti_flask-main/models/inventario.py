from datetime import datetime

from extensions import db


class FiltroPrivacidade(db.Model):
    __tablename__ = "filtros_privacidade"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    tipo = db.Column(
        db.String(30),
        nullable=False
    )

    tamanho = db.Column(
        db.String(30),
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    observacao = db.Column(
        db.String(255),
        nullable=True
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<FiltroPrivacidade "
            f"{self.tipo} - {self.tamanho}>"
        )


class DiscoCofre(db.Model):
    __tablename__ = "cofre_discos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    identificacao_maquina = db.Column(
        db.String(100),
        nullable=False
    )

    serial_disco = db.Column(
        db.String(150),
        nullable=True
    )

    fornecedor = db.Column(
        db.String(120),
        nullable=True
    )

    data_envio = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="Armazenado"
    )

    observacao = db.Column(
        db.String(255),
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

    def __repr__(self):
        return f"<DiscoCofre {self.identificacao_maquina}>"
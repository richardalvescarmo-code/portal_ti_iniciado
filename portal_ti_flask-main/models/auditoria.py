from datetime import datetime

from extensions import db


class Auditoria(db.Model):
    __tablename__ = "auditoria"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario = db.Column(
        db.String(120),
        nullable=False
    )

    acao = db.Column(
        db.String(50),
        nullable=False
    )

    modulo = db.Column(
        db.String(80),
        nullable=False
    )

    registro = db.Column(
        db.String(255),
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Auditoria "
            f"{self.usuario} - "
            f"{self.acao} - "
            f"{self.modulo}>"
        )
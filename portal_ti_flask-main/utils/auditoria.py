from extensions import db
from models.auditoria import Auditoria


def registrar_auditoria(
    usuario,
    modulo,
    acao,
    registro
):
    novo_registro = Auditoria(
        usuario=usuario,
        modulo=modulo,
        acao=acao,
        registro=registro
    )

    db.session.add(
        novo_registro
    )
    db.session.commit()
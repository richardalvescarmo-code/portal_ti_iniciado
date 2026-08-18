import os

from flask import Blueprint, send_from_directory
from flask_login import login_required


downloads_bp = Blueprint(
    "downloads",
    __name__
)


def _pasta(subpasta):
    # Fora de /static/ de proposito: assim o nginx nao serve o
    # arquivo direto, e todo download passa por esta rota, que
    # exige login. Ver e baixar continua liberado para qualquer
    # usuario autenticado; o que fechamos e o acesso anonimo.
    return os.path.join(
        os.getcwd(),
        "uploads",
        subpasta
    )


@downloads_bp.route("/download/softwares/<nome>")
@login_required
def baixar_software(nome):
    # send_from_directory bloqueia path traversal (../) sozinho.
    return send_from_directory(
        _pasta("softwares"),
        nome,
        as_attachment=True
    )


@downloads_bp.route("/download/procedimentos/<nome>")
@login_required
def baixar_procedimento(nome):
    return send_from_directory(
        _pasta("procedimentos"),
        nome
    )

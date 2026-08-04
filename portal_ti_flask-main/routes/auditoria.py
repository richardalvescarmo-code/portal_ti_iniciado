from flask import Blueprint, render_template
from flask_login import login_required

from models.auditoria import Auditoria
from utils.permissoes import perfis_permitidos


auditoria_bp = Blueprint(
    "auditoria",
    __name__
)


@auditoria_bp.route("/auditoria")
@login_required
@perfis_permitidos("administrador")
def auditoria():

    logs = Auditoria.query.order_by(
        Auditoria.data.desc()
    ).all()

    return render_template(
        "auditoria.html",
        logs=logs,
        active_page="auditoria"
    )
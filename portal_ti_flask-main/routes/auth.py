from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from extensions import db
from models import Usuario


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        usuario_digitado = request.form.get(
            "usuario",
            ""
        ).strip()

        senha_digitada = request.form.get(
            "senha",
            ""
        )

        usuario = Usuario.query.filter_by(
            usuario=usuario_digitado
        ).first()

        if (
            usuario
            and usuario.ativo
            and usuario.verificar_senha(senha_digitada)
        ):

            usuario.registrar_login()

            db.session.commit()

            login_user(
                usuario
            )

            proxima_pagina = request.args.get(
                "next"
            )

            if proxima_pagina:
                return redirect(
                    proxima_pagina
                )

            return redirect(
                url_for("dashboard.home")
            )

        flash(
            "Usuário ou senha inválidos.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "login.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )
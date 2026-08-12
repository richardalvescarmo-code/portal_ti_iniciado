from urllib.parse import urljoin, urlparse

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import (
    login_required,
    login_user,
    logout_user,
)

from extensions import db, limiter
from models import Usuario


auth_bp = Blueprint(
    "auth",
    __name__
)


def url_redirecionamento_segura(target):
    if not target:
        return False

    host_url = request.host_url

    url_base = urlparse(
        host_url
    )

    url_destino = urlparse(
        urljoin(
            host_url,
            target
        )
    )

    return (
        url_destino.scheme in ("http", "https")
        and url_base.netloc == url_destino.netloc
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
@limiter.limit(
    "5 per minute",
    methods=["POST"],
    error_message=(
        "Muitas tentativas de login. "
        "Aguarde um minuto e tente novamente."
    )
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
            and usuario.verificar_senha(
                senha_digitada
            )
        ):

            usuario.registrar_login()

            db.session.commit()

            login_user(
                usuario
            )

            # Faz a sessão respeitar
            # PERMANENT_SESSION_LIFETIME
            session.permanent = True

            proxima_pagina = request.args.get(
                "next"
            )

            if (
                proxima_pagina
                and url_redirecionamento_segura(
                    proxima_pagina
                )
            ):
                return redirect(
                    proxima_pagina
                )

            return redirect(
                url_for(
                    "dashboard.home"
                )
            )

        flash(
            "Usuário ou senha inválidos.",
            "danger"
        )

        return redirect(
            url_for(
                "auth.login"
            )
        )

    return render_template(
        "login.html"
    )


@auth_bp.route(
    "/logout"
)
@login_required
def logout():

    logout_user()

    session.clear()

    return redirect(
        url_for(
            "auth.login"
        )
    )
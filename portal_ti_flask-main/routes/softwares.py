from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models.softwares import Software
from utils.auditoria import registrar_auditoria


softwares_bp = Blueprint(
    "softwares",
    __name__
)


@softwares_bp.route("/softwares")
@login_required
def softwares():
    lista_softwares = Software.query.order_by(
        Software.nome.asc()
    ).all()

    return render_template(
        "softwares.html",
        softwares=lista_softwares,
        active_page="softwares"
    )


@softwares_bp.route(
    "/softwares/cadastrar",
    methods=["POST"]
)
@login_required
def cadastrar_software():
    nome = request.form.get(
        "nome",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    categoria = request.form.get(
        "categoria",
        ""
    ).strip()

    url_download = request.form.get(
        "url_download",
        ""
    ).strip()

    if not nome:
        flash(
            "Informe o nome do software.",
            "danger"
        )

        return redirect(
            url_for("softwares.softwares")
        )

    if not url_download:
        flash(
            "Informe o link para download.",
            "danger"
        )

        return redirect(
            url_for("softwares.softwares")
        )

    novo_software = Software(
        nome=nome,
        descricao=descricao or None,
        categoria=categoria or None,
        url_download=url_download,
        ativo=True
    )

    try:
        db.session.add(
            novo_software
        )

        registrar_auditoria(
            usuario=current_user.nome,
            modulo="Softwares",
            acao="Criou",
            registro=novo_software.nome
        )

        db.session.commit()

        flash(
            "Software cadastrado com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao cadastrar software: {erro}"
        )

        flash(
            "Não foi possível cadastrar o software.",
            "danger"
        )

    return redirect(
        url_for("softwares.softwares")
    )


@softwares_bp.route(
    "/softwares/<int:software_id>/editar",
    methods=["POST"]
)
@login_required
def editar_software(software_id):
    software = Software.query.get_or_404(
        software_id
    )

    nome = request.form.get(
        "nome",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    categoria = request.form.get(
        "categoria",
        ""
    ).strip()

    url_download = request.form.get(
        "url_download",
        ""
    ).strip()

    ativo = request.form.get(
        "ativo"
    ) == "on"

    if not nome:
        flash(
            "Informe o nome do software.",
            "danger"
        )

        return redirect(
            url_for("softwares.softwares")
        )

    if not url_download:
        flash(
            "Informe o link para download.",
            "danger"
        )

        return redirect(
            url_for("softwares.softwares")
        )

    software.nome = nome
    software.descricao = descricao or None
    software.categoria = categoria or None
    software.url_download = url_download
    software.ativo = ativo

    try:
        registrar_auditoria(
            usuario=current_user.nome,
            modulo="Softwares",
            acao="Editou",
            registro=software.nome
        )

        db.session.commit()

        flash(
            "Software atualizado com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao atualizar software: {erro}"
        )

        flash(
            "Não foi possível atualizar o software.",
            "danger"
        )

    return redirect(
        url_for("softwares.softwares")
    )


@softwares_bp.route(
    "/softwares/<int:software_id>/excluir",
    methods=["POST"]
)
@login_required
def excluir_software(software_id):
    software = Software.query.get_or_404(
        software_id
    )

    nome_software = software.nome

    try:
        db.session.delete(
            software
        )

        registrar_auditoria(
            usuario=current_user.nome,
            modulo="Softwares",
            acao="Excluiu",
            registro=nome_software
        )

        db.session.commit()

        flash(
            "Software excluído com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao excluir software: {erro}"
        )

        flash(
            "Não foi possível excluir o software.",
            "danger"
        )

    return redirect(
        url_for("softwares.softwares")
    )
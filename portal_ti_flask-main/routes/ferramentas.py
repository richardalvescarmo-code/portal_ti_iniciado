from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from utils.permissoes import perfis_permitidos
from extensions import db
from models.ferramentas import Ferramenta


ferramentas_bp = Blueprint(
    "ferramentas",
    __name__
)


@ferramentas_bp.route("/ferramentas")
@login_required
def ferramentas():

    lista_ferramentas = Ferramenta.query.order_by(
        Ferramenta.nome.asc()
    ).all()

    return render_template(
        "ferramentas.html",
        ferramentas=lista_ferramentas,
        active_page="ferramentas"
    )


@ferramentas_bp.route(
    "/ferramentas/cadastrar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def cadastrar_ferramenta():

    nome = request.form.get(
        "nome",
        ""
    ).strip()

    categoria = request.form.get(
        "categoria",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    url_acesso = request.form.get(
        "url_acesso",
        ""
    ).strip()

    icone = request.form.get(
        "icone",
        "bi-tools"
    ).strip()

    if not nome:
        flash(
            "Informe o nome da ferramenta.",
            "danger"
        )

        return redirect(
            url_for("ferramentas.ferramentas")
        )

    if not url_acesso:
        flash(
            "Informe o link de acesso.",
            "danger"
        )

        return redirect(
            url_for("ferramentas.ferramentas")
        )

    if not icone:
        icone = "bi-tools"

    nova_ferramenta = Ferramenta(
        nome=nome,
        categoria=categoria or None,
        descricao=descricao or None,
        url_acesso=url_acesso,
        icone=icone,
        ativo=True
    )

    try:
        db.session.add(nova_ferramenta)
        db.session.commit()

        flash(
            "Ferramenta cadastrada com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao cadastrar ferramenta: {erro}"
        )

        flash(
            "Não foi possível cadastrar a ferramenta.",
            "danger"
        )

    return redirect(
        url_for("ferramentas.ferramentas")
    )


@ferramentas_bp.route(
    "/ferramentas/<int:ferramenta_id>/editar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def editar_ferramenta(ferramenta_id):

    ferramenta = Ferramenta.query.get_or_404(
        ferramenta_id
    )

    nome = request.form.get(
        "nome",
        ""
    ).strip()

    categoria = request.form.get(
        "categoria",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    url_acesso = request.form.get(
        "url_acesso",
        ""
    ).strip()

    icone = request.form.get(
        "icone",
        "bi-tools"
    ).strip()

    ativo = request.form.get(
        "ativo"
    ) == "on"

    if not nome:
        flash(
            "Informe o nome da ferramenta.",
            "danger"
        )

        return redirect(
            url_for("ferramentas.ferramentas")
        )

    if not url_acesso:
        flash(
            "Informe o link de acesso.",
            "danger"
        )

        return redirect(
            url_for("ferramentas.ferramentas")
        )

    ferramenta.nome = nome
    ferramenta.categoria = categoria or None
    ferramenta.descricao = descricao or None
    ferramenta.url_acesso = url_acesso
    ferramenta.icone = icone or "bi-tools"
    ferramenta.ativo = ativo

    try:
        db.session.commit()

        flash(
            "Ferramenta atualizada com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao atualizar ferramenta: {erro}"
        )

        flash(
            "Não foi possível atualizar a ferramenta.",
            "danger"
        )

    return redirect(
        url_for("ferramentas.ferramentas")
    )


@ferramentas_bp.route(
    "/ferramentas/<int:ferramenta_id>/excluir",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def excluir_ferramenta(ferramenta_id):

    ferramenta = Ferramenta.query.get_or_404(
        ferramenta_id
    )

    try:
        db.session.delete(ferramenta)
        db.session.commit()

        flash(
            "Ferramenta excluída com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao excluir ferramenta: {erro}"
        )

        flash(
            "Não foi possível excluir a ferramenta.",
            "danger"
        )

    return redirect(
        url_for("ferramentas.ferramentas")
    )
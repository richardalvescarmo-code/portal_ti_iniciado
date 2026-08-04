import os
from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from extensions import db
from models.procedimentos import Procedimento


procedimentos_bp = Blueprint(
    "procedimentos",
    __name__
)


EXTENSOES_PERMITIDAS = {
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "png",
    "jpg",
    "jpeg",
    "zip"
}


def extensao_permitida(nome_arquivo):
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS
    )


def pasta_uploads():
    return os.path.join(
        os.getcwd(),
        "static",
        "uploads",
        "procedimentos"
    )


def salvar_arquivo(arquivo):
    if not arquivo or not arquivo.filename:
        return None, None

    if not extensao_permitida(arquivo.filename):
        raise ValueError(
            "Formato de arquivo não permitido."
        )

    nome_original = secure_filename(
        arquivo.filename
    )

    extensao = nome_original.rsplit(
        ".",
        1
    )[1].lower()

    nome_salvo = f"{uuid4().hex}.{extensao}"

    os.makedirs(
        pasta_uploads(),
        exist_ok=True
    )

    caminho_completo = os.path.join(
        pasta_uploads(),
        nome_salvo
    )

    arquivo.save(
        caminho_completo
    )

    return nome_salvo, nome_original


def excluir_arquivo(nome_arquivo):
    if not nome_arquivo:
        return

    caminho_completo = os.path.join(
        pasta_uploads(),
        nome_arquivo
    )

    if os.path.exists(caminho_completo):
        os.remove(caminho_completo)


@procedimentos_bp.route("/procedimentos")
@login_required
def procedimentos():

    lista_procedimentos = Procedimento.query.order_by(
        Procedimento.titulo.asc()
    ).all()

    return render_template(
        "procedimentos.html",
        procedimentos=lista_procedimentos,
        active_page="procedimentos"
    )


@procedimentos_bp.route(
    "/procedimentos/cadastrar",
    methods=["POST"]
)
@login_required
def cadastrar_procedimento():

    titulo = request.form.get(
        "titulo",
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

    conteudo = request.form.get(
        "conteudo",
        ""
    ).strip()

    arquivo = request.files.get(
        "arquivo"
    )

    if not titulo:
        flash(
            "Informe o título do procedimento.",
            "danger"
        )

        return redirect(
            url_for("procedimentos.procedimentos")
        )

    if not conteudo:
        flash(
            "Informe o passo a passo.",
            "danger"
        )

        return redirect(
            url_for("procedimentos.procedimentos")
        )

    nome_salvo = None
    nome_original = None

    try:
        nome_salvo, nome_original = salvar_arquivo(
            arquivo
        )

        novo = Procedimento(
            titulo=titulo,
            categoria=categoria or None,
            descricao=descricao or None,
            conteudo=conteudo,
            arquivo_nome=nome_salvo,
            arquivo_original=nome_original,
            ativo=True
        )

        db.session.add(novo)
        db.session.commit()

        flash(
            "Procedimento cadastrado com sucesso.",
            "success"
        )

    except ValueError as erro:
        excluir_arquivo(
            nome_salvo
        )

        flash(
            str(erro),
            "danger"
        )

    except Exception as erro:
        db.session.rollback()

        excluir_arquivo(
            nome_salvo
        )

        print(
            f"Erro ao cadastrar procedimento: {erro}"
        )

        flash(
            "Não foi possível cadastrar o procedimento.",
            "danger"
        )

    return redirect(
        url_for("procedimentos.procedimentos")
    )


@procedimentos_bp.route(
    "/procedimentos/<int:procedimento_id>/editar",
    methods=["POST"]
)
@login_required
def editar_procedimento(procedimento_id):

    procedimento = Procedimento.query.get_or_404(
        procedimento_id
    )

    titulo = request.form.get(
        "titulo",
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

    conteudo = request.form.get(
        "conteudo",
        ""
    ).strip()

    ativo = request.form.get(
        "ativo"
    ) == "on"

    arquivo = request.files.get(
        "arquivo"
    )

    remover_arquivo = request.form.get(
        "remover_arquivo"
    ) == "on"

    if not titulo:
        flash(
            "Informe o título do procedimento.",
            "danger"
        )

        return redirect(
            url_for("procedimentos.procedimentos")
        )

    if not conteudo:
        flash(
            "Informe o passo a passo.",
            "danger"
        )

        return redirect(
            url_for("procedimentos.procedimentos")
        )

    novo_nome_salvo = None
    novo_nome_original = None
    arquivo_antigo = procedimento.arquivo_nome

    try:
        if arquivo and arquivo.filename:
            novo_nome_salvo, novo_nome_original = salvar_arquivo(
                arquivo
            )

            procedimento.arquivo_nome = novo_nome_salvo
            procedimento.arquivo_original = novo_nome_original

        elif remover_arquivo:
            procedimento.arquivo_nome = None
            procedimento.arquivo_original = None

        procedimento.titulo = titulo
        procedimento.categoria = categoria or None
        procedimento.descricao = descricao or None
        procedimento.conteudo = conteudo
        procedimento.ativo = ativo

        db.session.commit()

        if novo_nome_salvo or remover_arquivo:
            excluir_arquivo(
                arquivo_antigo
            )

        flash(
            "Procedimento atualizado com sucesso.",
            "success"
        )

    except ValueError as erro:
        excluir_arquivo(
            novo_nome_salvo
        )

        flash(
            str(erro),
            "danger"
        )

    except Exception as erro:
        db.session.rollback()

        excluir_arquivo(
            novo_nome_salvo
        )

        print(
            f"Erro ao atualizar procedimento: {erro}"
        )

        flash(
            "Não foi possível atualizar o procedimento.",
            "danger"
        )

    return redirect(
        url_for("procedimentos.procedimentos")
    )


@procedimentos_bp.route(
    "/procedimentos/<int:procedimento_id>/excluir",
    methods=["POST"]
)
@login_required
def excluir_procedimento(procedimento_id):

    procedimento = Procedimento.query.get_or_404(
        procedimento_id
    )

    arquivo_nome = procedimento.arquivo_nome

    try:
        db.session.delete(procedimento)
        db.session.commit()

        excluir_arquivo(
            arquivo_nome
        )

        flash(
            "Procedimento excluído com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao excluir procedimento: {erro}"
        )

        flash(
            "Não foi possível excluir o procedimento.",
            "danger"
        )

    return redirect(
        url_for("procedimentos.procedimentos")
    )
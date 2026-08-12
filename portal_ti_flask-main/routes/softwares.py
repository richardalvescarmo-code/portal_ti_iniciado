import os
from uuid import uuid4

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from extensions import db
from models.softwares import Software
from utils.auditoria import registrar_auditoria


softwares_bp = Blueprint(
    "softwares",
    __name__
)


def pasta_uploads():
    return os.path.join(
        os.getcwd(),
        "static",
        "uploads",
        "softwares"
    )


def salvar_executavel(arquivo):
    if not arquivo or not arquivo.filename:
        return None, None

    nome_original = secure_filename(
        arquivo.filename
    )

    if not nome_original.lower().endswith(".exe"):
        raise ValueError(
            "Somente arquivos .exe são permitidos."
        )

    nome_salvo = f"{uuid4().hex}.exe"

    os.makedirs(
        pasta_uploads(),
        exist_ok=True
    )

    caminho = os.path.join(
        pasta_uploads(),
        nome_salvo
    )

    arquivo.save(
        caminho
    )

    return nome_salvo, nome_original


def excluir_executavel(nome_arquivo):
    if not nome_arquivo:
        return

    caminho = os.path.join(
        pasta_uploads(),
        nome_arquivo
    )

    if os.path.exists(caminho):
        os.remove(caminho)


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

    arquivo = request.files.get(
        "arquivo"
    )

    if not nome:
        flash(
            "Informe o nome do software.",
            "danger"
        )

        return redirect(
            url_for("softwares.softwares")
        )

    if not url_download and not (arquivo and arquivo.filename):
        flash(
            "Informe um link para download ou anexe um arquivo .exe.",
            "danger"
        )

        return redirect(
            url_for("softwares.softwares")
        )

    nome_salvo = None
    nome_original = None

    try:
        nome_salvo, nome_original = salvar_executavel(
            arquivo
        )

        novo_software = Software(
            nome=nome,
            descricao=descricao or None,
            categoria=categoria or None,
            url_download=url_download or None,
            arquivo_nome=nome_salvo,
            arquivo_original=nome_original,
            ativo=True
        )

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

    except ValueError as erro:
        excluir_executavel(
            nome_salvo
        )

        flash(
            str(erro),
            "danger"
        )

    except Exception as erro:
        db.session.rollback()

        excluir_executavel(
            nome_salvo
        )

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

    arquivo = request.files.get(
        "arquivo"
    )

    remover_arquivo = request.form.get(
        "remover_arquivo"
    ) == "on"

    if not nome:
        flash(
            "Informe o nome do software.",
            "danger"
        )

        return redirect(
            url_for("softwares.softwares")
        )

    arquivo_antigo = software.arquivo_nome

    novo_nome_salvo = None
    novo_nome_original = None

    try:
        if arquivo and arquivo.filename:
            novo_nome_salvo, novo_nome_original = salvar_executavel(
                arquivo
            )

            software.arquivo_nome = novo_nome_salvo
            software.arquivo_original = novo_nome_original

        elif remover_arquivo:
            software.arquivo_nome = None
            software.arquivo_original = None

        software.nome = nome
        software.descricao = descricao or None
        software.categoria = categoria or None
        software.url_download = url_download or None
        software.ativo = ativo

        if not software.url_download and not software.arquivo_nome:
            raise ValueError(
                "O software precisa ter um link ou um arquivo .exe."
            )

        registrar_auditoria(
            usuario=current_user.nome,
            modulo="Softwares",
            acao="Editou",
            registro=software.nome
        )

        db.session.commit()

        if novo_nome_salvo or remover_arquivo:
            excluir_executavel(
                arquivo_antigo
            )

        flash(
            "Software atualizado com sucesso.",
            "success"
        )

    except ValueError as erro:
        db.session.rollback()

        excluir_executavel(
            novo_nome_salvo
        )

        flash(
            str(erro),
            "danger"
        )

    except Exception as erro:
        db.session.rollback()

        excluir_executavel(
            novo_nome_salvo
        )

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
    arquivo_nome = software.arquivo_nome

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

        excluir_executavel(
            arquivo_nome
        )

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
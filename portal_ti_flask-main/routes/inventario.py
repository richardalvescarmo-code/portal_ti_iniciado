from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from utils.permissoes import perfis_permitidos
from extensions import db
from models.inventario import DiscoCofre, FiltroPrivacidade


inventario_bp = Blueprint(
    "inventario",
    __name__
)


@inventario_bp.route("/inventario")
@login_required
def inventario():

    filtros = FiltroPrivacidade.query.order_by(
        FiltroPrivacidade.tipo.asc(),
        FiltroPrivacidade.tamanho.asc()
    ).all()

    discos = DiscoCofre.query.order_by(
        DiscoCofre.criado_em.desc()
    ).all()

    return render_template(
        "inventario.html",
        filtros=filtros,
        discos=discos,
        active_page="inventario"
    )


@inventario_bp.route(
    "/inventario/filtros/cadastrar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def cadastrar_filtro():

    tipo = request.form.get(
        "tipo",
        ""
    ).strip()

    tamanho = request.form.get(
        "tamanho",
        ""
    ).strip()

    quantidade = request.form.get(
        "quantidade",
        "0"
    ).strip()

    observacao = request.form.get(
        "observacao",
        ""
    ).strip()

    if tipo not in {
        "Notebook",
        "Desktop"
    }:
        flash(
            "Selecione um tipo de filtro válido.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    if not tamanho:
        flash(
            "Informe o tamanho do filtro.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    try:
        quantidade = int(
            quantidade
        )

        if quantidade < 0:
            raise ValueError

    except ValueError:
        flash(
            "Informe uma quantidade válida.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    filtro_existente = FiltroPrivacidade.query.filter_by(
        tipo=tipo,
        tamanho=tamanho
    ).first()

    if filtro_existente:
        flash(
            "Já existe um filtro cadastrado com esse tipo e tamanho.",
            "warning"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    novo_filtro = FiltroPrivacidade(
        tipo=tipo,
        tamanho=tamanho,
        quantidade=quantidade,
        observacao=observacao or None
    )

    try:
        db.session.add(
            novo_filtro
        )

        db.session.commit()

        flash(
            "Filtro de privacidade cadastrado com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao cadastrar filtro: {erro}"
        )

        flash(
            "Não foi possível cadastrar o filtro.",
            "danger"
        )

    return redirect(
        url_for("inventario.inventario")
    )


@inventario_bp.route(
    "/inventario/filtros/<int:filtro_id>/editar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def editar_filtro(filtro_id):

    filtro = FiltroPrivacidade.query.get_or_404(
        filtro_id
    )

    tipo = request.form.get(
        "tipo",
        ""
    ).strip()

    tamanho = request.form.get(
        "tamanho",
        ""
    ).strip()

    quantidade = request.form.get(
        "quantidade",
        "0"
    ).strip()

    observacao = request.form.get(
        "observacao",
        ""
    ).strip()

    if tipo not in {
        "Notebook",
        "Desktop"
    }:
        flash(
            "Selecione um tipo de filtro válido.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    if not tamanho:
        flash(
            "Informe o tamanho do filtro.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    try:
        quantidade = int(
            quantidade
        )

        if quantidade < 0:
            raise ValueError

    except ValueError:
        flash(
            "Informe uma quantidade válida.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    duplicado = FiltroPrivacidade.query.filter(
        FiltroPrivacidade.tipo == tipo,
        FiltroPrivacidade.tamanho == tamanho,
        FiltroPrivacidade.id != filtro.id
    ).first()

    if duplicado:
        flash(
            "Já existe outro filtro cadastrado com esse tipo e tamanho.",
            "warning"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    filtro.tipo = tipo
    filtro.tamanho = tamanho
    filtro.quantidade = quantidade
    filtro.observacao = observacao or None

    try:
        db.session.commit()

        flash(
            "Filtro atualizado com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao atualizar filtro: {erro}"
        )

        flash(
            "Não foi possível atualizar o filtro.",
            "danger"
        )

    return redirect(
        url_for("inventario.inventario")
    )


@inventario_bp.route(
    "/inventario/filtros/<int:filtro_id>/excluir",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def excluir_filtro(filtro_id):

    filtro = FiltroPrivacidade.query.get_or_404(
        filtro_id
    )

    try:
        db.session.delete(
            filtro
        )

        db.session.commit()

        flash(
            "Filtro de privacidade excluído com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao excluir filtro: {erro}"
        )

        flash(
            "Não foi possível excluir o filtro.",
            "danger"
        )

    return redirect(
        url_for("inventario.inventario")
    )


@inventario_bp.route(
    "/inventario/cofre/cadastrar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def cadastrar_disco():

    identificacao_maquina = request.form.get(
        "identificacao_maquina",
        ""
    ).strip()

    serial_disco = request.form.get(
        "serial_disco",
        ""
    ).strip()

    fornecedor = request.form.get(
        "fornecedor",
        ""
    ).strip()

    data_envio = request.form.get(
        "data_envio",
        ""
    ).strip()

    status = request.form.get(
        "status",
        "Armazenado"
    ).strip()

    observacao = request.form.get(
        "observacao",
        ""
    ).strip()

    if not identificacao_maquina:
        flash(
            "Informe a identificação da máquina.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    data_envio_convertida = None

    if data_envio:
        try:
            data_envio_convertida = datetime.strptime(
                data_envio,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            flash(
                "Informe uma data de envio válida.",
                "danger"
            )

            return redirect(
                url_for("inventario.inventario")
            )

    novo_disco = DiscoCofre(
        identificacao_maquina=identificacao_maquina,
        serial_disco=serial_disco or None,
        fornecedor=fornecedor or None,
        data_envio=data_envio_convertida,
        status=status or "Armazenado",
        observacao=observacao or None
    )

    try:
        db.session.add(
            novo_disco
        )

        db.session.commit()

        flash(
            "Disco cadastrado no cofre com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao cadastrar disco: {erro}"
        )

        flash(
            "Não foi possível cadastrar o disco.",
            "danger"
        )

    return redirect(
        url_for("inventario.inventario")
    )


@inventario_bp.route(
    "/inventario/cofre/<int:disco_id>/editar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def editar_disco(disco_id):

    disco = DiscoCofre.query.get_or_404(
        disco_id
    )

    identificacao_maquina = request.form.get(
        "identificacao_maquina",
        ""
    ).strip()

    serial_disco = request.form.get(
        "serial_disco",
        ""
    ).strip()

    fornecedor = request.form.get(
        "fornecedor",
        ""
    ).strip()

    data_envio = request.form.get(
        "data_envio",
        ""
    ).strip()

    status = request.form.get(
        "status",
        "Armazenado"
    ).strip()

    observacao = request.form.get(
        "observacao",
        ""
    ).strip()

    if not identificacao_maquina:
        flash(
            "Informe a identificação da máquina.",
            "danger"
        )

        return redirect(
            url_for("inventario.inventario")
        )

    data_envio_convertida = None

    if data_envio:
        try:
            data_envio_convertida = datetime.strptime(
                data_envio,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            flash(
                "Informe uma data de envio válida.",
                "danger"
            )

            return redirect(
                url_for("inventario.inventario")
            )

    disco.identificacao_maquina = identificacao_maquina
    disco.serial_disco = serial_disco or None
    disco.fornecedor = fornecedor or None
    disco.data_envio = data_envio_convertida
    disco.status = status or "Armazenado"
    disco.observacao = observacao or None

    try:
        db.session.commit()

        flash(
            "Disco atualizado com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao atualizar disco: {erro}"
        )

        flash(
            "Não foi possível atualizar o disco.",
            "danger"
        )

    return redirect(
        url_for("inventario.inventario")
    )


@inventario_bp.route(
    "/inventario/cofre/<int:disco_id>/excluir",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def excluir_disco(disco_id):

    disco = DiscoCofre.query.get_or_404(
        disco_id
    )

    try:
        db.session.delete(
            disco
        )

        db.session.commit()

        flash(
            "Disco excluído do cofre com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao excluir disco: {erro}"
        )

        flash(
            "Não foi possível excluir o disco.",
            "danger"
        )

    return redirect(
        url_for("inventario.inventario")
    )
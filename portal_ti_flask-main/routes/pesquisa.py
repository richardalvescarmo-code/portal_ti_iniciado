from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import or_

from models.ferramentas import Ferramenta
from models.inventario import DiscoCofre
from models.procedimentos import Procedimento
from models.softwares import Software


pesquisa_bp = Blueprint(
    "pesquisa",
    __name__
)


@pesquisa_bp.route("/pesquisa")
@login_required
def pesquisa():

    termo = request.args.get(
        "q",
        ""
    ).strip()

    resultados = {
        "softwares": [],
        "procedimentos": [],
        "ferramentas": [],
        "discos": [],
    }

    if termo:
        busca = f"%{termo}%"

        resultados["softwares"] = Software.query.filter(
            or_(
                Software.nome.ilike(busca),
                Software.categoria.ilike(busca),
                Software.descricao.ilike(busca)
            )
        ).all()

        resultados["procedimentos"] = Procedimento.query.filter(
            or_(
                Procedimento.titulo.ilike(busca),
                Procedimento.categoria.ilike(busca),
                Procedimento.descricao.ilike(busca),
                Procedimento.conteudo.ilike(busca)
            )
        ).all()

        resultados["ferramentas"] = Ferramenta.query.filter(
            or_(
                Ferramenta.nome.ilike(busca),
                Ferramenta.categoria.ilike(busca),
                Ferramenta.descricao.ilike(busca)
            )
        ).all()

        resultados["discos"] = DiscoCofre.query.filter(
            or_(
                DiscoCofre.identificacao_maquina.ilike(busca),
                DiscoCofre.serial_disco.ilike(busca),
                DiscoCofre.fornecedor.ilike(busca),
                DiscoCofre.status.ilike(busca),
                DiscoCofre.observacao.ilike(busca)
            )
        ).all()

    total_resultados = sum(
        len(lista)
        for lista in resultados.values()
    )

    return render_template(
        "pesquisa.html",
        termo=termo,
        resultados=resultados,
        total_resultados=total_resultados,
        active_page=""
    )
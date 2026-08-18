from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from extensions import db


preferencias_bp = Blueprint(
    "preferencias",
    __name__
)


# Lista branca. O valor recebido vai parar em um atributo HTML,
# entao aceitar qualquer string abriria espaco para injecao.
# Validar contra um conjunto fechado e mais seguro e mais barato
# do que tentar limpar a entrada depois.
TEMAS_VALIDOS = {
    "claro",
    "escuro"
}

CORES_VALIDAS = {
    "azul",
    "verde",
    "roxo",
    "laranja",
    "vermelho"
}


@preferencias_bp.route(
    "/preferencias/aparencia",
    methods=["POST"]
)
@login_required
def salvar_aparencia():

    dados = request.get_json(silent=True) or {}

    tema = dados.get("tema")

    cor = dados.get("cor")

    if tema is not None:

        if tema not in TEMAS_VALIDOS:
            return jsonify(
                {"erro": "Tema invalido."}
            ), 400

        current_user.tema = tema

    if cor is not None:

        if cor not in CORES_VALIDAS:
            return jsonify(
                {"erro": "Cor invalida."}
            ), 400

        current_user.cor_primaria = cor

    db.session.commit()

    return jsonify({
        "tema": current_user.tema,
        "cor": current_user.cor_primaria
    })

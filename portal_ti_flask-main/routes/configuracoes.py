import os

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import or_, text

from extensions import db
from models import Usuario
from models.ferramentas import Ferramenta
from models.inventario import (
    DiscoCofre,
    FiltroPrivacidade,
)
from models.procedimentos import Procedimento
from models.softwares import Software
from utils.permissoes import perfis_permitidos


configuracoes_bp = Blueprint(
    "configuracoes",
    __name__
)


PERFIS_VALIDOS = {
    "administrador",
    "analista",
    "estagiario"
}


def usuario_duplicado(
    usuario,
    email,
    ignorar_id=None
):
    consulta = Usuario.query.filter(
        or_(
            Usuario.usuario == usuario,
            Usuario.email == email
        )
    )

    if ignorar_id is not None:
        consulta = consulta.filter(
            Usuario.id != ignorar_id
        )

    return consulta.first()


def validar_senha_usuario(senha):
    senha_valida, mensagem = Usuario.validar_senha(
        senha
    )

    if not senha_valida:
        flash(
            mensagem,
            "danger"
        )

        return False

    return True


@configuracoes_bp.route("/configuracoes")
@login_required
@perfis_permitidos("administrador")
def configuracoes():

    banco_conectado = False

    try:
        db.session.execute(
            text("SELECT 1")
        )

        banco_conectado = True

    except Exception as erro:
        print(
            f"Erro ao verificar banco: {erro}"
        )

    totais = {
        "softwares": Software.query.count(),
        "procedimentos": Procedimento.query.count(),
        "ferramentas": Ferramenta.query.count(),
        "discos": DiscoCofre.query.count(),
        "filtros": FiltroPrivacidade.query.count(),
        "usuarios": Usuario.query.count(),
    }

    usuarios = Usuario.query.order_by(
        Usuario.nome.asc()
    ).all()

    pasta_uploads = os.path.join(
        os.getcwd(),
        "static",
        "uploads"
    )

    return render_template(
        "configuracoes.html",
        active_page="configuracoes",
        banco_conectado=banco_conectado,
        totais=totais,
        pasta_uploads=pasta_uploads,
        usuarios=usuarios
    )


@configuracoes_bp.route(
    "/configuracoes/usuarios/cadastrar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def cadastrar_usuario():

    nome = request.form.get(
        "nome",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    usuario_login = request.form.get(
        "usuario",
        ""
    ).strip().lower()

    perfil = request.form.get(
        "perfil",
        "analista"
    ).strip().lower()

    senha = request.form.get(
        "senha",
        ""
    )

    confirmar_senha = request.form.get(
        "confirmar_senha",
        ""
    )

    if not nome or not email or not usuario_login:
        flash(
            "Preencha nome, e-mail e usuário.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    if perfil not in PERFIS_VALIDOS:
        flash(
            "Selecione um perfil válido.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    if senha != confirmar_senha:
        flash(
            "A confirmação da senha não confere.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    if not validar_senha_usuario(
        senha
    ):
        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    duplicado = usuario_duplicado(
        usuario_login,
        email
    )

    if duplicado:
        flash(
            "Já existe um usuário com esse login ou e-mail.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        usuario=usuario_login,
        perfil=perfil,
        ativo=True
    )

    try:
        novo_usuario.definir_senha(
            senha
        )

        db.session.add(
            novo_usuario
        )

        db.session.commit()

        flash(
            "Usuário cadastrado com sucesso.",
            "success"
        )

    except ValueError as erro:
        db.session.rollback()

        flash(
            str(erro),
            "danger"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao cadastrar usuário: {erro}"
        )

        flash(
            "Não foi possível cadastrar o usuário.",
            "danger"
        )

    return redirect(
        url_for(
            "configuracoes.configuracoes"
        )
    )


@configuracoes_bp.route(
    "/configuracoes/usuarios/<int:usuario_id>/editar",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def editar_usuario(usuario_id):

    usuario = Usuario.query.get_or_404(
        usuario_id
    )

    nome = request.form.get(
        "nome",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    usuario_login = request.form.get(
        "usuario",
        ""
    ).strip().lower()

    perfil = request.form.get(
        "perfil",
        "analista"
    ).strip().lower()

    ativo = request.form.get(
        "ativo"
    ) == "on"

    if not nome or not email or not usuario_login:
        flash(
            "Preencha nome, e-mail e usuário.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    if perfil not in PERFIS_VALIDOS:
        flash(
            "Selecione um perfil válido.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    duplicado = usuario_duplicado(
        usuario_login,
        email,
        ignorar_id=usuario.id
    )

    if duplicado:
        flash(
            "Já existe outro usuário com esse login ou e-mail.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    if usuario.id == current_user.id:
        ativo = True

    usuario.nome = nome
    usuario.email = email
    usuario.usuario = usuario_login
    usuario.perfil = perfil
    usuario.ativo = ativo

    try:
        db.session.commit()

        flash(
            "Usuário atualizado com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao atualizar usuário: {erro}"
        )

        flash(
            "Não foi possível atualizar o usuário.",
            "danger"
        )

    return redirect(
        url_for(
            "configuracoes.configuracoes"
        )
    )


@configuracoes_bp.route(
    "/configuracoes/usuarios/<int:usuario_id>/redefinir-senha",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def redefinir_senha_usuario(usuario_id):

    usuario = Usuario.query.get_or_404(
        usuario_id
    )

    nova_senha = request.form.get(
        "nova_senha",
        ""
    )

    confirmar_senha = request.form.get(
        "confirmar_senha",
        ""
    )

    if nova_senha != confirmar_senha:
        flash(
            "A confirmação da senha não confere.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    if not validar_senha_usuario(
        nova_senha
    ):
        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    try:
        usuario.definir_senha(
            nova_senha
        )

        db.session.commit()

        flash(
            f"Senha de {usuario.nome} redefinida com sucesso.",
            "success"
        )

    except ValueError as erro:
        db.session.rollback()

        flash(
            str(erro),
            "danger"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao redefinir senha: {erro}"
        )

        flash(
            "Não foi possível redefinir a senha.",
            "danger"
        )

    return redirect(
        url_for(
            "configuracoes.configuracoes"
        )
    )


@configuracoes_bp.route(
    "/configuracoes/usuarios/<int:usuario_id>/excluir",
    methods=["POST"]
)
@login_required
@perfis_permitidos("administrador")
def excluir_usuario(usuario_id):

    usuario = Usuario.query.get_or_404(
        usuario_id
    )

    if usuario.id == current_user.id:
        flash(
            "Você não pode excluir o próprio usuário conectado.",
            "danger"
        )

        return redirect(
            url_for(
                "configuracoes.configuracoes"
            )
        )

    try:
        db.session.delete(
            usuario
        )

        db.session.commit()

        flash(
            "Usuário excluído com sucesso.",
            "success"
        )

    except Exception as erro:
        db.session.rollback()

        print(
            f"Erro ao excluir usuário: {erro}"
        )

        flash(
            "Não foi possível excluir o usuário.",
            "danger"
        )

    return redirect(
        url_for(
            "configuracoes.configuracoes"
        )
    )
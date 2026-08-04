from functools import wraps

from flask import abort
from flask_login import current_user


def perfis_permitidos(*perfis):
    def decorator(funcao):

        @wraps(funcao)
        def funcao_protegida(*args, **kwargs):

            perfil_usuario = (
                current_user.perfil or ""
            ).lower()

            perfis_normalizados = {
                perfil.lower()
                for perfil in perfis
            }

            if perfil_usuario not in perfis_normalizados:
                abort(403)

            return funcao(
                *args,
                **kwargs
            )

        return funcao_protegida

    return decorator
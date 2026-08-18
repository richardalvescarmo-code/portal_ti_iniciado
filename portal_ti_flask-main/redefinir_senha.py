from getpass import getpass

from app import app
from extensions import db
from models import Usuario

with app.app_context():
    print("\nUsuarios cadastrados:")
    for u in Usuario.query.order_by(Usuario.id):
        print(f"  [{u.id}] {u.usuario:20} {u.email:45} {u.perfil}")

    alvo = input("\nID do usuario: ").strip()
    usuario = db.session.get(Usuario, int(alvo))

    if not usuario:
        raise SystemExit("Usuario nao encontrado.")

    nova = getpass(f"Nova senha para '{usuario.usuario}': ")

    usuario.definir_senha(nova)
    db.session.commit()

    print(f"Senha de '{usuario.usuario}' atualizada.")

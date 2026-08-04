from app import app
from extensions import db
from models import Usuario


USUARIO_ADMIN = "admin"
EMAIL_ADMIN = "admin@portalti.local"
SENHA_ADMIN = "Admin@123"


with app.app_context():
    administrador_existente = Usuario.query.filter_by(
        usuario=USUARIO_ADMIN
    ).first()

    if administrador_existente:
        print("O usuário administrador já existe.")

    else:
        administrador = Usuario(
            nome="Administrador",
            email=EMAIL_ADMIN,
            usuario=USUARIO_ADMIN,
            perfil="administrador",
            ativo=True,
        )

        administrador.definir_senha(SENHA_ADMIN)

        db.session.add(administrador)
        db.session.commit()

        print("Administrador criado com sucesso!")
        print(f"Usuário: {USUARIO_ADMIN}")
        print(f"Senha inicial: {SENHA_ADMIN}")
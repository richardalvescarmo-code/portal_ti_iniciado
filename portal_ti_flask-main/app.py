from flask import Flask
from sqlalchemy import text

from config import Config
from extensions import db, login_manager
from models.usuario import Usuario
from routes import (
    auditoria_bp,
    auth_bp,
    configuracoes_bp,
    dashboard_bp,
    ferramentas_bp,
    inventario_bp,
    pesquisa_bp,
    procedimentos_bp,
    softwares_bp,
)


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    registrar_blueprints(app)
    registrar_login_manager()
    registrar_rotas_temporarias(app)

    return app


def registrar_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(softwares_bp)
    app.register_blueprint(procedimentos_bp)
    app.register_blueprint(ferramentas_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(configuracoes_bp)
    app.register_blueprint(pesquisa_bp)
    app.register_blueprint(auditoria_bp)


def registrar_login_manager():
    @login_manager.user_loader
    def carregar_usuario(usuario_id):
        return db.session.get(
            Usuario,
            int(usuario_id)
        )


def registrar_rotas_temporarias(app):
    @app.route("/teste-banco")
    def teste_banco():
        resultado = db.session.execute(
            text("SELECT DATABASE() AS banco")
        ).mappings().first()

        return {
            "status": "conectado",
            "banco": resultado["banco"]
        }


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
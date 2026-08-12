from flask import Flask, request
from sqlalchemy import text

from config import Config
from extensions import csrf, db, limiter, login_manager
from models.usuario import Usuario
from routes import (
    auth_bp,
    auditoria_bp,
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
    csrf.init_app(app)
    limiter.init_app(app)

    registrar_blueprints(app)
    registrar_login_manager()
    registrar_rotas_temporarias(app)
    registrar_headers_seguranca(app)
    registrar_erros(app)

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


def registrar_headers_seguranca(app):
    @app.after_request
    def adicionar_headers(response):

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        response.headers["Referrer-Policy"] = (
            "strict-origin-when-cross-origin"
        )

        response.headers["Permissions-Policy"] = (
            "camera=(), "
            "microphone=(), "
            "geolocation=()"
        )

        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net; "
            "font-src 'self' "
            "https://cdn.jsdelivr.net data:; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'self'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )

        if request.is_secure:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response


def registrar_erros(app):
    @app.errorhandler(413)
    def arquivo_muito_grande(erro):
        return (
            "O arquivo enviado excede o tamanho máximo permitido.",
            413
        )


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=False
    )
from flask import Blueprint, render_template
from flask_login import login_required

from models.auditoria import Auditoria
from models.ferramentas import Ferramenta
from models.inventario import DiscoCofre
from models.procedimentos import Procedimento
from models.softwares import Software
from models.usuario import Usuario


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
@login_required
def home():

    integrations = [
        {
            "name": "TOPdesk",
            "description": (
                "Sistema de chamados e atendimento da equipe de TI."
            ),
            "icon": "bi-headset",
            "url": "https://itsmabr.topdesk.net/",
        },
        {
            "name": "Planner - Demandas do Dia",
            "description": (
                "Quadro de tarefas e demandas diárias da equipe."
            ),
            "icon": "bi-kanban",
            "url": (
                "https://planner.cloud.microsoft/webui/plan/"
                "QzZfJMDkg0OGU1-dGEcPXGQABLyA/view/board"
                "?tid=682718e1-a242-4f2e-a523-292c8b2362eb"
            ),
        },
        {
            "name": "Grafana",
            "description": (
                "Dashboards, alertas e monitoramento dos serviços."
            ),
            "icon": "bi-graph-up-arrow",
            "url": "https://grafana.hugtak.com/",
        },
        {
            "name": "Intune",
            "description": (
                "Gerenciamento e conformidade dos dispositivos."
            ),
            "icon": "bi-laptop",
            "url": (
                "https://intune.microsoft.com/"
                "?ref=AdminCenter#home"
            ),
        },
        {
            "name": "SharePoint",
            "description": (
                "Acesso aos sites e documentos corporativos."
            ),
            "icon": "bi-folder2-open",
            "url": "https://abrtelecom.sharepoint.com/",
        },
        {
            "name": "Exchange Admin",
            "description": (
                "Administração de caixas de correio e permissões."
            ),
            "icon": "bi-envelope",
            "url": (
                "https://admin.exchange.microsoft.com/"
                "#/homepage"
            ),
        },
        {
            "name": "Microsoft 365 Admin",
            "description": (
                "Administração dos serviços Microsoft 365."
            ),
            "icon": "bi-microsoft",
            "url": (
                "https://admin.cloud.microsoft/"
                "?source=applauncher#/homepage"
            ),
        },
    ]

    resumo = {
        "softwares": Software.query.count(),
        "procedimentos": Procedimento.query.count(),
        "ferramentas": Ferramenta.query.count(),
        "discos": DiscoCofre.query.count(),
        "usuarios": Usuario.query.count(),
    }

    ultimas_atividades = Auditoria.query.order_by(
        Auditoria.data.desc()
    ).limit(5).all()

    return render_template(
        "home.html",
        integrations=integrations,
        resumo=resumo,
        ultimas_atividades=ultimas_atividades,
        active_page="home"
    )
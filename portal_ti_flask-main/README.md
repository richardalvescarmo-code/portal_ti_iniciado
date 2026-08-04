# Portal TI

Portal interno desenvolvido com Flask, SQLAlchemy e Bootstrap.

## Executar localmente

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Estado atual

- Estrutura Flask organizada com Blueprint.
- Configuração de banco por variável de ambiente.
- SQLite como fallback local e suporte a MySQL.
- Dashboard responsivo.
- Módulos separados para TOPdesk, Intune, Exchange, Grafana, Planner e Microsoft Graph.
- Integrações ainda sem credenciais ou chamadas reais.

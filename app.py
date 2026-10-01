from flask import Flask, jsonify

from main import LOGS, ler_evento, contar_falhas_por_ip, detectar_suspeitos, formatar_alerta

app = Flask(__name__)


def gerar_relatorio():
    eventos = [ler_evento(linha) for linha in LOGS]
    return detectar_suspeitos(contar_falhas_por_ip(eventos))


@app.route("/")
def index():
    alertas = [formatar_alerta(ip, total) for ip, total in gerar_relatorio().items()]
    return "<h1>Relatório de autenticação</h1>" + "<br>".join(alertas)


@app.route("/api/alertas")
def api_alertas():
    # Mesmo relatório em JSON, como uma ferramenta de monitoração consumiria
    return jsonify(gerar_relatorio())


if __name__ == "__main__":
    # 0.0.0.0 para aceitar conexões vindas do host, não só de dentro do container
    app.run(host="0.0.0.0", port=5000)
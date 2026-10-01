# Analisador simples de logs de autenticação.
# Formato de cada linha: DATA HORA STATUS usuario=X ip=Y

LOGS = [
    "2026-10-01 08:12:01 FALHA usuario=admin ip=192.168.0.10",
    "2026-10-01 08:12:05 FALHA usuario=admin ip=192.168.0.10",
    "2026-10-01 08:12:09 FALHA usuario=root ip=192.168.0.10",
    "2026-10-01 08:13:40 SUCESSO usuario=gabriel ip=192.168.0.25",
    "2026-10-01 08:15:02 FALHA usuario=maria ip=192.168.0.31",
    "2026-10-01 08:15:20 SUCESSO usuario=maria ip=192.168.0.31",
    "2026-10-01 08:16:44 FALHA usuario=admin ip=10.0.0.99",
    "2026-10-01 08:16:47 FALHA usuario=admin ip=10.0.0.99",
    "2026-10-01 08:16:50 FALHA usuario=admin ip=10.0.0.99",
    "2026-10-01 08:16:53 FALHA usuario=admin ip=10.0.0.99",
]


def ler_evento(linha):
    """Transforma uma linha de log em um dicionário."""
    partes = linha.split()
    # As três primeiras partes têm posição fixa: data, hora e status
    evento = {"data": partes[0], "hora": partes[1], "status": partes[2]}
    # O resto são pares chave=valor. O 1 no split quebra só no primeiro "=",
    # assim um valor que contenha "=" não estraga a leitura
    for par in partes[3:]:
        chave, valor = par.split("=", 1)
        evento[chave] = valor
    return evento


if __name__ == "__main__":
    for linha in LOGS:
        evento = ler_evento(linha)
        print(f"{evento['hora']} {evento['status']} {evento['usuario']} {evento['ip']}")
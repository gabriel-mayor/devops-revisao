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
    evento = {"data": partes[0], "hora": partes[1], "status": partes[2]}
    for par in partes[3:]:
        chave, valor = par.split("=", 1)
        evento[chave] = valor
    return evento


def contar_falhas_por_ip(eventos):
    """Conta quantas falhas de login cada IP teve. Percorre a lista uma vez: O(n)."""
    contagem = {}
    for evento in eventos:
        if evento["status"] == "FALHA":
            # get devolve 0 se o IP ainda não está no dicionário
            contagem[evento["ip"]] = contagem.get(evento["ip"], 0) + 1
    return contagem


def detectar_suspeitos(contagem, limite=3):
    """Retorna só os IPs que atingiram o limite de falhas."""
    return {ip: total for ip, total in contagem.items() if total >= limite}


if __name__ == "__main__":
    eventos = [ler_evento(linha) for linha in LOGS]
    suspeitos = detectar_suspeitos(contar_falhas_por_ip(eventos))
    for ip, total in suspeitos.items():
        print(f"IP suspeito: {ip} ({total} falhas)")
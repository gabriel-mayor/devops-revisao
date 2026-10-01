from main import LOGS, ler_evento, contar_falhas_por_ip, detectar_suspeitos, formatar_alerta


def test_ler_evento():
    evento = ler_evento("2026-10-01 08:12:01 FALHA usuario=admin ip=192.168.0.10")
    assert evento["status"] == "FALHA"
    assert evento["usuario"] == "admin"
    assert evento["ip"] == "192.168.0.10"


def test_contar_falhas_por_ip():
    eventos = [ler_evento(linha) for linha in LOGS]
    assert contar_falhas_por_ip(eventos) == {
        "192.168.0.10": 3,
        "192.168.0.31": 1,
        "10.0.0.99": 4,
    }


def test_detectar_suspeitos():
    contagem = {"192.168.0.10": 3, "192.168.0.31": 1, "10.0.0.99": 4}
    assert detectar_suspeitos(contagem) == {"192.168.0.10": 3, "10.0.0.99": 4}


def test_formatar_alerta():
    assert formatar_alerta("10.0.0.99", 4) == (
        "[ALERTA] Possível força bruta: 10.0.0.99 com 4 falhas de login"
    )
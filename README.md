# Revisão Integração DevOps

![CI](https://github.com/GabrielMSM2/devops-revisao/actions/workflows/ci.yml/badge.svg)

Projeto da revisão da disciplina de Integração DevOps (questões 23 a 28), cobrindo Git, GitHub Actions, processos e portas, e Docker.

A aplicação é um analisador simples de logs de autenticação. Ela lê eventos de login, conta as falhas por IP e gera um alerta quando um IP atinge 3 falhas, indicando possível ataque de força bruta. É a mesma lógica de threshold usada em regras de alerta de um SIEM.

## Estrutura

| Arquivo | Função |
|---|---|
| `main.py` | Leitura dos logs, contagem de falhas e detecção de IPs suspeitos |
| `test_main.py` | Testes automatizados com pytest |
| `app.py` | Aplicação Flask que expõe o relatório no navegador e em JSON |
| `Dockerfile` | Receita para construir a imagem da aplicação |
| `requirements.txt` | Dependências da aplicação |
| `.github/workflows/ci.yml` | Workflow de integração contínua |

## Como executar

Direto com Python:

```
python main.py
python -m pytest
```

Com Docker:

```
docker build -t devops-revisao .
docker run -d -p 8080:5000 --name revisao devops-revisao
```

Depois acessar `http://localhost:8080` ou `http://localhost:8080/api/alertas`.

## 23. Repositório Git e commits

Repositório criado com `git init -b main`. Cada etapa do trabalho foi registrada em um commit com mensagem descritiva.

Saída do `git log --oneline`:

```
(cole aqui)
```

## 24. Branch feature-mensagem

Foi criada a branch `feature-mensagem` para alterar a saída do programa, que passou a exibir os resultados no formato de alerta. Depois a branch foi integrada à `main`.

```
git switch -c feature-mensagem
git add main.py
git commit -m "Altera saída para formato de alerta"
git switch main
git merge feature-mensagem
```

## 25. GitHub Actions

O workflow em `.github/workflows/ci.yml` roda a cada push e executa as etapas de checkout do código, configuração do Python 3, instalação do pytest e execução dos testes. O resultado pode ser conferido na aba Actions do repositório.

## 26. Porta e PID

Servidor iniciado em um terminal com `python -m http.server 8080`. Em outro terminal, a porta e o PID foram identificados, o processo foi confirmado antes de ser encerrado e a liberação da porta foi verificada.

Identificação da porta e do PID:

```
netstat -ano | findstr :8080
(cole aqui)
```

Confirmação do processo:

```
tasklist /FI "PID eq <PID>"
(cole aqui)
```

Encerramento:

```
taskkill /PID <PID> /F
(cole aqui)
```

Verificação final (sem retorno, indicando que a porta foi liberada):

```
netstat -ano | findstr :8080
```

## 27. Dockerfile

O `Dockerfile` usa a imagem base `python:3.12-slim`, define `/app` como diretório de trabalho, copia e instala as dependências, copia os arquivos da aplicação e define `python app.py` como comando de inicialização.

O `requirements.txt` é copiado antes do restante dos arquivos para aproveitar o cache de camadas do Docker. Assim, quando só o código muda, a instalação das dependências não precisa ser refeita.

## 28. Build e execução do container

```
docker build -t devops-revisao .
docker run -d -p 8080:5000 --name revisao devops-revisao
docker ps
docker logs revisao
```

Saída do `docker ps`:

```
CONTAINER ID   IMAGE            COMMAND           CREATED         STATUS         PORTS                                         NAMES
a318808d8445   devops-revisao   "python app.py"   9 minutes ago   Up 4 seconds   0.0.0.0:8080->5000/tcp, [::]:8080->5000/tcp   revisao
```

Saída do `docker logs`:

```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

A opção `-p 8080:5000` mapeia a porta 8080 do host para a porta 5000 do container. A aplicação escuta em `0.0.0.0` para aceitar conexões vindas de fora do container. Se escutasse apenas em `127.0.0.1`, ficaria inacessível pelo navegador do host.

### Problema encontrado

Durante os testes o container apareceu com status `Exited (137)` no `docker ps -a`. Pelo `docker logs` foi possível ver que a aplicação tinha subido normalmente em `0.0.0.0:5000`. O código 137 indica que o processo foi encerrado por SIGKILL (128 + 9), o que aconteceu porque o container foi parado com `docker stop` antes do teste no navegador. O container foi reiniciado com `docker start revisao` e a aplicação ficou acessível.

### Observação

A aplicação usa o servidor de desenvolvimento do Flask, adequado para fins de estudo. Em produção seria usado um servidor WSGI, como o Gunicorn.
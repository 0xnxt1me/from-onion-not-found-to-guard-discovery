# 3_cell-pattern: Guia rápido anotamentos

## Para que serve este diretório?
Contém scripts, configs e dados para estudar o padrão de células Tor quando se faz lookup de onion não existente ("404 Not Found").

## README principal
Explica como construir os containers Docker necessários para os experimentos e garante que tudo é reprodutível (versões fixas).

## determinism
Testa se o padrão de ataque é sempre igual (determinístico) usando redes pequenas e controladas. Roda vários experimentos Shadow e analisa os logs para confirmar que o padrão aparece sempre que esperado.

## uniqueness
Testa se o padrão de ataque aparece só nos ataques (é único) usando uma rede Tor simulada grande (2% do real). Gera centenas de logs e analisa todos para garantir que o padrão não ocorre naturalmente.

### Nota sobre espaço em disco
Para rodar o uniqueness ocupando menos espaço (ex: menos de 35 GB), gere uma rede Tor simulada menor (ex: 0.5% ou 1%).

**Passos simples:**
1. Vá para o diretório do Dockerfile:
    ```bash
    cd 3_cell-pattern/docker-builds
    ```
2. Edite o arquivo `Dockerfile.tornetgen` e troque o parâmetro `--network_scale` na linha do comando `tornetgen generate` para o valor desejado, por exemplo:
    ```
    RUN tornetgen generate ... --network_scale 0.005 --prefix tornet-0.005
    ```
3. Salve o Dockerfile e reconstrua a imagem:
    ```bash
    sudo docker build -t ubuntu-tornetgen-tor -f Dockerfile.tornetgen .
    ```
4. Volte para o diretório onde quer salvar os dados e rode o container:
    ```bash
    cd 3_cell-pattern/uniqueness
    mkdir tornettools_2020-05-data
    sudo chmod -R 777 tornettools_2020-05-data
    sudo docker run --rm \
         -v "$(pwd)"/tornettools_2020-05-data:/tor-network-generation \
         ubuntu-tornetgen-tor:latest
    ```
Pronto! Assim você gera uma rede menor e economiza espaço.

---
Use estes diretórios para reproduzir, analisar e validar os resultados dos experimentos descritos no paper.

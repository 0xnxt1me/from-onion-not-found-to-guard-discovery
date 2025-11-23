# Experimento Uniqueness com 0.5% Rede Tor - Setup Completo

## Objetivo
Testar se o padrão de ataque de células Tor (404 Not Found) é único usando rede simulada de 0.5% (menor que os 2% originais) para economizar espaço em disco.

## Passos Executados

### 1. Gerar rede simulada com TorNetTools (0.5%)

**Dockerfile modificação:**
- Editou `Dockerfile.tornetgen` para mudar `--network_scale 0.02` → `--network_scale 0.005`
- Mudou prefixo `tornet-0.02` → `tornet-0.005`
- **Importante**: Corrigir o `CMD` final para copiar `tornettools/tornet-0.005` (não 0.02)

**Execução:**
```bash
cd 3_cell-pattern/docker-builds
sudo docker build -t ubuntu-tornetgen-tor -f Dockerfile.tornetgen .

cd ../uniqueness
mkdir tornettools_2020-05-data
sudo chmod -R 777 tornettools_2020-05-data
sudo docker run --rm \
    -v "$(pwd)"/tornettools_2020-05-data:/tor-network-generation \
    ubuntu-tornetgen-tor:latest
```

**Output esperado:**
- Pasta `tornettools_2020-05-data/tornet-0.005/` com:
  - `shadow.config.xml` (~85 KB)
  - `conf/atlas-lossless.201801.shadow113.graphml.xml` (~450 MB)
  - `shadow.data.template/` com hosts

### 2. Montar experimento Shadow com topologia gerada

**Copiar arquivos:**
```bash
cd 3_cell-pattern/uniqueness/shadow-plugin-tor_0.5-perc-scale-tor

# Copiar topologia
cp /home/nxt/Desktop/Fac/1sem/SR/SR_TP/from-onion-not-found-to-guard-discovery/3_cell-pattern/uniqueness/tornettools_2020-05-data/tornet-0.005/conf/atlas-lossless.201801.shadow113.graphml.xml resource/shadowtor-0.5-perc-scale-tor/conf/

# Copiar shadow.data.template
cp -r /home/nxt/Desktop/Fac/1sem/SR/SR_TP/from-onion-not-found-to-guard-discovery/3_cell-pattern/uniqueness/tornettools_2020-05-data/tornet-0.005/shadow.data.template/* resource/shadowtor-0.5-perc-scale-tor/shadow.data.template/

# Garantir permissões
sudo chmod -R 777 resource/shadowtor-0.5-perc-scale-tor/
```

### 3. Rodar simulação Shadow

```bash
mkdir cell_counters_reproduced

sudo docker run --rm \
    -v "$(pwd)"/resource/shadowtor-0.5-perc-scale-tor:/experiment \
    -v "$(pwd)"/cell_counters_reproduced:/home/shadow/cell_counters \
    ubuntu-shadow-tgen-tor-cellcounters:latest
```

**Tempo estimado:** Várias horas (depende do hardware)
**Output:** Logs de cell counters em `cell_counters_reproduced/`

## Próximos Passos

### 4. Analisar logs coletados
```bash
../shadow_exps_find_adv_pattern_workstation.sh ./cell_counters_reproduced
```

### 5. Verificar resultados
```bash
grep "2ND_HOP_RESULT" cell_counters_reproduced_analyzed/* | grep "No adversarial"
grep "3RD_HOP_RESULT" cell_counters_reproduced_analyzed/* | grep "No adversarial"
```

**Resultado esperado:** Todos os logs devem indicar que o padrão NÃO foi encontrado (confirma que é único)

## Fixes Principais Aplicados

| Problema | Solução |
|----------|---------|
| Scientific notation no CSV | Adicionar preprocessing no Dockerfile.tornetgen |
| CMD Dockerfile copiava prefixo errado | Mudar `tornet-0.02` → `tornet-0.005` |
| Topologia não gerada | Garantir que Dockerfile executa `tornetgen generate` completamente |
| Permissões de acesso | `sudo chmod -R 777` nas pastas montadas |
| Arquivo graphml faltava | Copiar do output do TorNetTools para a pasta conf do Shadow |

## Próximos Testes Sugeridos

1. **Testar com consensos 2025** (em vez de 2020-05)
   - Modificar `Dockerfile.tornetgen` para usar dados mais recentes
   - Repetir o mesmo pipeline com dados atualizados

2. **Verificar reprodutibilidade**
   - Rodar novamente com mesma configuração
   - Comparar resultados

3. **Explorar diferentes escalas**
   - Testar 0.2%, 0.5%, 1% para ver impacto
   - Documentar tamanho vs tempo de execução

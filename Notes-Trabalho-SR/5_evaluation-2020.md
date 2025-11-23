# 5_evaluation - Avaliação do Ataque (Dados 2020)

## Objetivo
Testar o ataque "From Onion Not Found to Guard Discovery" usando dados de 2020 para validar os resultados do paper e depois comparar com dados de 2025.

## O que o 5_evaluation faz
Simula o ataque completo usando **scripts Python** (não precisa de Shadow/Docker), medindo:
1. Taxa de lookup de ruído do Tor
2. Sucesso do ataque (probabilidade de descobrir guards)
3. Tempo para gerar chaves públicas do ataque

## Passos para Rodar com Dados 2020

### 0. Pré-requisitos
```bash
cd /home/nxt/Desktop/Fac/1sem/SR/SR_TP/from-onion-not-found-to-guard-discovery/5_evaluation

# Instalar dependências
pip3 install --user numpy jupyter matplotlib pandas
```

### 1. Analisar Taxa de Lookup de Ruído (Noise Lookup Rate)

**O que faz:** Analisa quantos lookups "naturais" (não-ataque) acontecem na rede Tor.

**Executar:**
```bash
jupyter lab
# Abrir e rodar: 1_analysis_noise-lookup-rate.ipynb
```

**Dados usados:**
- `1_data_noise-lookup-rate/` - Contagens de códigos de resposta HSDir

**Resultado esperado:** Taxa de ~1052 lookups/segundo (valor usado no paper)

---

### 2. Simular Sucesso do Ataque

**O que faz:** Simula o ataque variando parâmetros (nº guards adversariais, fração da rede) e mede probabilidade de sucesso.

**Parâmetros do script:**
- `N_EXPERIMENTS_TO_REPLAY`: Quantos experimentos usar (-1 = todos)
- `N_RUNS`: Quantas repetições por experimento

**Executar simulação completa (como no paper):**
```bash
# Rodar todas as combinações de parâmetros
# Isso roda 9 simulações em paralelo (3 adversários × 3 frações)
./2_script_run-simulation.sh -1 50 > sim_results_2020_all_50.log
```

**Executar teste rápido (menos tempo):**
```bash
# Rodar 10 experimentos amostrados, 10 repetições cada
./2_script_run-simulation.sh 10 10 > sim_results_2020_test.log
```

**Parâmetros testados:**
- Adversários controlando: 1, 2 ou 6 guards
- Fração da rede controlada: 1%, 2% ou 5%

**Dados usados:**
- `2020-09-22-18-36-48_relays.csv` - Lista de relays Tor (Set 2020)
- `hsdesc_lookup_details.json` - Timestamps de lookups de experimentos reais

**Output:**
- Logs com resultados de sucesso para cada configuração
- Salvo em `2_data_attack-time/`

**Analisar resultados:**
```bash
jupyter lab
# Abrir e rodar: 2_analysis_attack-time.ipynb
```

**Resultado esperado (do paper):**
- Com 6 guards adversariais e 5% da rede: ~80-90% sucesso
- Tempo médio para descobrir guard: ~X minutos

---

### 3. Medir Tempo de Geração de Chaves Públicas

**O que faz:** Mede quanto tempo demora para gerar chaves públicas de onion services que mapearão para HSDirs adversariais específicos.

**Configurar script:**
Editar `gen_atk_pubkeys.py` no topo:
```python
NUM_WORKER_PROCS = 8  # Ajustar para nº de threads disponíveis
NUM_ADV_HSDIRS = [1, 2, 6, 12, 24]  # Nº de HSDirs adversariais
NUM_REPETITIONS = 10  # Quantas vezes repetir cada configuração
```

**Executar:**
```bash
mkdir output_gen-atk-pubkeys

python3 gen_atk_pubkeys.py \
    --state_dir ./3_data_consensus-descriptors \
    --out_dir ./output_gen-atk-pubkeys
```

**Tempo estimado:** Várias horas (16h no paper com config padrão)

**Dados usados:**
- `3_data_consensus-descriptors/` - Estado da rede Tor (consensos 2020)

**Output:**
- Tempos de geração para diferentes nº de HSDirs adversariais
- Salvo em `output_gen-atk-pubkeys/`

**Analisar resultados:**
```bash
jupyter lab
# Abrir e rodar: 3_analysis_generate-attack-public-keys.ipynb
```

**Resultado esperado (do paper):**
- Tempo cresce exponencialmente com nº de HSDirs
- Para 6 HSDirs: ~X minutos

---

## Estrutura de Dados Fornecidos (2020)

```
5_evaluation/
├── 1_data_noise-lookup-rate/          # Dados de taxa de ruído
├── 2_data_attack-time/                 # Resultados de simulação de ataque
├── 3_data_consensus-descriptors/       # Consensos Tor Set 2020
├── 3_data_generate-attack-public-keys/ # Resultados de geração de chaves
├── 2020-09-22-18-36-48_relays.csv     # Lista de relays Set 2020
├── hsdesc_lookup_details.json          # Timestamps de lookups
└── attack_simulation.py                # Script principal de simulação
```

## Resumo dos Comandos (Teste Rápido)

```bash
cd 5_evaluation

# 1. Simulação rápida (10 experimentos, 10 runs)
./2_script_run-simulation.sh 10 10 > sim_results_quick.log

# 2. Ver progresso
tail -f sim_results_quick.log

# 3. Analisar nos notebooks
jupyter lab
# Rodar: 2_analysis_attack-time.ipynb
```

## Próximos Passos

Após validar com dados de 2020:
1. Comparar resultados com as figuras/tabelas do paper
2. Adaptar para dados de 2025 (atualizar relay list e consensos)
3. Comparar resultados 2020 vs 2025

## Interpretação dos Resultados

### Ficheiros JSON gerados: `time_to_double_comp_X_Y_Z_W.json`

**Nome do ficheiro:** `time_to_double_comp_{n_adv_hsdirs}_{adv_bw_share}_{n_initial_tokens}_{token_refill_rate}.json`

**Exemplo:** `time_to_double_comp_6_0.05_0_0.000.json`
- `6` = 6 guards adversariais
- `0.05` = 5% da bandwidth da rede controlada
- `0` = 0 tokens iniciais (sem rate limiting)
- `0.000` = taxa de refill de tokens (sem vanguards-lite)

**Conteúdo do JSON:**
```json
{
  "n_experiments": 10,           // Quantos experimentos foram simulados
  "n_runs": 10,                   // Quantas repetições por experimento
  "n_adv_hsdirs": 6,             // Guards adversariais
  "adv_bw_share": 0.05,          // 5% da rede controlada
  "attack_durations": [...]       // Lista de tempos (segundos) até descobrir guard
}
```

**Métricas importantes:**
- `attack_durations`: Lista de quanto tempo (segundos) demorou para descobrir o guard da vítima em cada run
- Se valor = `300`: Ataque falhou (timeout)

### Ficheiro de log: `sim_results_2020_test.log`

**Exemplo de linha:**
```
Runs: 100: (h: 1.00, bw: 0.05, tb_iv: 0, tb_rr:  0.00)
Median: 6.917, P90: 12.894, P99: 15.362 (FP-single: 17.38%)
FINAL-CALLS - T: 100.00% F: 0.00% Nocall: 0.00%
```

**Significado:**
- `h: 1.00` = 6/6 guards adversariais (100% dos 6 guards)
- `bw: 0.05` = 5% da bandwidth da rede
- `Median: 6.917` = Tempo mediano para descobrir guard: **6.9 segundos** 🎯
- `P90: 12.894` = 90% dos ataques descobrem em ≤12.9s
- `P99: 15.362` = 99% dos ataques descobrem em ≤15.4s
- `FP-single: 17.38%` = Taxa de falsos positivos (single-hop)
- `T: 100.00%` = **100% dos ataques tiveram sucesso** ✅
- `F: 0.00%` = 0% falharam
- `Nocall: 0.00%` = 0% sem resultado

### Conclusões dos Resultados (Teste com 10 experimentos, 10 runs cada)

| Adversários | Bandwidth | Mediana (s) | P90 (s) | Taxa Sucesso |
|-------------|-----------|-------------|---------|--------------|
| 1 guard | 1% | 91.0 | 235.4 | 98% |
| 1 guard | 2% | 40.3 | 114.7 | 100% |
| 1 guard | 5% | 17.1 | 36.4 | 100% |
| 2 guards | 1% | 42.6 | 131.2 | 99% |
| 2 guards | 2% | 21.8 | 63.9 | 100% |
| 2 guards | 5% | 12.4 | 21.7 | 100% |
| **6 guards** | 1% | 16.3 | 27.4 | 99% |
| **6 guards** | 2% | 12.2 | 21.6 | 100% |
| **6 guards** | **5%** | **6.9** | **12.9** | **100%** ✅ |

**Conclusão chave:**
- ✅ Com 6 guards adversariais e 5% da rede: ataque descobre guard em **~7 segundos** (mediana)
- ✅ Taxa de sucesso: **100%** (todos os ataques funcionaram)
- ✅ Mesmo com 1 guard e 1% da rede: 98% de sucesso em ~1.5 minutos

**Comparar com o paper:**
- Os valores obtidos devem bater com as figuras do paper (Section 5.3)
- Usar notebooks Jupyter para gerar gráficos comparativos

## Scripts de Análise Criados

### `analyze_results.py` - Análise Rápida
Analisa todos os ficheiros JSON e gera tabela com estatísticas:
```bash
python3 analyze_results.py
```

**Output:**
- Tabela comparativa de todos os cenários
- Destaca melhor/pior/realista casos
- Conclusões sobre eficácia do ataque

### `plot_results.py` - Gráficos Visuais
Gera gráficos de comparação:
```bash
python3 plot_results.py
```

**Output:**
- `attack_time_comparison_2020.png` - Box plots de tempo por configuração
- `attack_success_rate_2020.png` - Barras de taxa de sucesso

## Análise Final - Resultados 2020

### Contexto da Rede Tor (Setembro 2020)

```
Total de Relays: 6451
Total de HSDirs: 3905
HSDirs por Onion: 6
Noise Lookups: 1052.27 lookups/segundo
```

### Resultados dos Nossos Testes (10 experimentos × 10 runs)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Guards │   BW   │ Sucesso │ Mediana │  Mean  │   P90   │   P99   │  Runs    │
├──────────────────────────────────────────────────────────────────────────────┤
│   1    │   1.0% │   98.0% │   90.1s │  104.2s │   229.5s │   271.5s │ 98/100 │
│   1    │   2.0% │  100.0% │   40.3s │   56.1s │   114.7s │   204.4s │ 100/100│
│   1    │   5.0% │  100.0% │   17.1s │   21.1s │    36.4s │    66.6s │ 100/100│
│   2    │   1.0% │   99.0% │   42.4s │   58.2s │   127.4s │   233.3s │ 99/100 │
│   2    │   2.0% │  100.0% │   21.8s │   29.4s │    63.9s │   114.7s │ 100/100│
│   2    │   5.0% │  100.0% │   12.4s │   13.7s │    21.7s │    42.5s │ 100/100│
│   6    │   1.0% │  100.0% │   16.3s │   19.0s │    27.4s │    62.2s │ 100/100│
│   6    │   2.0% │  100.0% │   12.2s │   13.4s │    21.6s │    56.5s │ 100/100│
│   6    │   5.0% │  100.0% │    6.9s │    7.6s │    12.9s │    15.4s │ 100/100│
└──────────────────────────────────────────────────────────────────────────────┘
```

### Comparação: Paper Original vs. Nossos Testes

**Dados do Paper** (2867 experimentos × 100 runs, extraídos de `2_data_attack-time/attack-success_sim.log`):

| Configuração      | Paper Mediana | Nosso Mediana | Diferença | Paper Sucesso | Nosso Sucesso |
|-------------------|---------------|---------------|-----------|---------------|---------------|
| 1 guard + 1% BW   | 88.6s         | 90.1s         | +1.5s     | 93.10%        | 98.0%         |
| 1 guard + 2% BW   | 40.0s         | 40.3s         | +0.3s     | 98.90%        | 100.0%        |
| 1 guard + 5% BW   | 18.5s         | 17.1s         | -1.4s     | 99.63%        | 100.0%        |
| 2 guards + 1% BW  | 39.9s         | 42.4s         | +2.5s     | 98.85%        | 99.0%         |
| 2 guards + 2% BW  | 21.7s         | 21.8s         | +0.1s     | 99.50%        | 100.0%        |
| **2 guards + 5% BW** | **12.1s**  | **12.4s**    | **+0.3s** | **99.78%**    | **100.0%**    |
| 6 guards + 1% BW  | 16.4s         | 16.3s         | -0.1s     | 99.42%        | 100.0%        |
| 6 guards + 2% BW  | 10.9s         | 12.2s         | +1.3s     | 99.63%        | 100.0%        |
| 6 guards + 5% BW  | 6.7s          | 6.9s          | +0.2s     | 99.75%        | 100.0%        |

**Nota sobre probabilidades de HSDir:**
- 1 guard adversarial = 1/6 = 16.67% probabilidade
- 2 guards adversariais = 2/6 = 33.33% probabilidade (configuração "realista" do paper)
- 6 guards adversariais = 6/6 = 100% probabilidade (cenário "best case")

### Validação dos Resultados

**Diferenças mínimas:** Entre 0.1s e 2.5s de diferença nas medianas

**Mesma ordem de grandeza:** Todos os tempos comparáveis

**Taxa de sucesso igual/superior:** Nossos testes atingiram 98-100% sucesso

**Consistência:** Resultados confirmam claims do paper (Section 5.3)

**Conclusão:** Os nossos resultados **reproduzem fielmente** os resultados do paper original, validando a eficácia do ataque mesmo com apenas 10 experimentos (vs. 2867 do paper).

### Porque o Ataque é Tão Rápido?

O ataque consegue descobrir o guard node em ~10-12 segundos devido a:

1. **Alta taxa de noise lookups:** 1052 lookups/segundo na rede Tor real
2. **Probabilidade favorável:** Com 2/6 guards adversariais = 33% chance de interceptar
3. **Bandwidth modesta suficiente:** 5% da rede já garante observação frequente
4. **Threshold baixo:** Apenas 2 matches do mesmo guard são necessários para confirmar

**Configuração recomendada pelo paper (2 guards + 5% BW):**
- Tempo mediano: **12.4 segundos**
- Taxa de sucesso: **100%**
- 90% dos ataques completam em ≤21.7s
- Representa cenário "realista" com recursos modestos

### Insights Principais

1. **O ataque é extremamente eficaz:**
   - Mesmo no pior cenário (1 guard, 1% BW): 98% sucesso em ~90s
   - Cenários com ≥2% bandwidth: 100% sucesso
   - **Os tempos curtos (~10-20s) são reais e confirmados pelo paper**

2. **Escalabilidade com recursos:**
   - Dobrar guards (1→2): reduz tempo ~50-60%
   - Aumentar bandwidth (1%→5%): reduz tempo ~70-80%
   - Combinação de ambos: ataque extremamente rápido (<7s)

3. **Viabilidade prática:**
   - Atacante com recursos modestos (2 guards, 2% BW): sucesso em ~22s
   - Não requer controlo massivo da rede
   - Taxa de falsos positivos aceitável (~19%)

4. **Implicações de segurança:**
   - Ataque viável mesmo para adversários com recursos limitados
   - Tempo de ataque suficientemente curto para ser prático
   - Justifica necessidade de countermeasures (Section 6 do paper)

## Notas Importantes

- **Espaço em disco:** < 5 GB (muito menos que 3_cell-pattern)
- **Tempo de execução:**
  - Simulação completa: ~1-2 horas
  - Geração de chaves: 16+ horas (opcional)
- **CPU:** Quanto mais cores, mais rápido (paralelização)
- Os dados de 2020 já estão incluídos no repositório
- **Resultados:** Ficheiros JSON com tempos + log com estatísticas agregadas
- **Gráficos:** Gerados automaticamente para visualização

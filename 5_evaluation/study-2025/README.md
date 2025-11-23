# Study 2025 - Guard Discovery Attack Validation

Estudo temporal para validar a persistência da vulnerabilidade "Guard Discovery" em 2025.

## 📁 Estrutura

```
study-2025/
├── scripts/          # Scripts Python criados para o estudo
├── data/            # Dados Tor de 2025 (consensus + relay CSV)
├── results/         # Resultados das simulações JSON
├── graphs/          # Visualizações geradas
└── README.md        # Este ficheiro
```

---

## 📜 `/scripts/` - Scripts Criados

### `download_consensus_2025.py`
**Propósito:** Download do consensus Tor atual do Tor Collector
**Input:** URL do Tor Collector API
**Output:** `../data/consensus_2025/consensus-2025-11-23`

```bash
python3 scripts/download_consensus_2025.py
```

**Nota:** Teve problemas de timeout com stem API, usado wget como alternativa.

---

### `process_consensus_2025.py`
**Propósito:** Processar consensus e gerar CSV de relays compatível com `attack_simulation.py`
**Input:** `data/consensus_2025/consensus-2025-11-23`
**Output:** `data/2025-11-23_relays.csv` (9186 relays)

```bash
python3 scripts/process_consensus_2025.py
```

**Lógica de classificação:**
- Exit > Guard > Middle (prioridade exclusiva)
- Guards têm `guard_probability` E `middle_probability` (podem ser middle hops)
- Cálculo de probabilidades segue o modelo do paper original

---

### `compare_2020_vs_2025.py`
**Propósito:** Comparação side-by-side dos resultados 2020 vs 2025
**Input:**
- `../2_data_attack-time/time_to_double_comp_*.json` (2020)
- `results/time_to_double_comp_*.json` (2025)

**Output:** Tabela formatada no terminal

```bash
python3 scripts/compare_2020_vs_2025.py
```

**Métricas calculadas:**
- Mediana de tempo de ataque
- Taxa de sucesso (%)
- Diferença temporal entre anos

---

## 📊 `/data/` - Dados Tor 2025

### `2025-11-23_relays.csv`
- **9186 relays** (vs 6451 em 2020)
- **5007 HSDirs** (vs 3905 em 2020)
- Crescimento: **+42.4% relays**, **+28.2% HSDirs**

**Colunas:**
```
nickname,fingerprint,published,address,or_port,dir_port,bandwidth,
exit_probability,guard_probability,middle_probability,is_hs_dir
```

### `consensus_2025/consensus-2025-23`
- Consensus Tor de 23 Nov 2025
- Tamanho: 3.9 MB
- Fonte: https://collector.torproject.org/

---

## 📈 `/results/` - Resultados das Simulações

9 ficheiros JSON (3 guards × 3 bandwidth shares):

```
time_to_double_comp_1_0.01_0_0.000.json  # 1 guard,  1% BW
time_to_double_comp_1_0.02_0_0.000.json  # 1 guard,  2% BW
time_to_double_comp_1_0.05_0_0.000.json  # 1 guard,  5% BW
time_to_double_comp_2_0.01_0_0.000.json  # 2 guards, 1% BW
time_to_double_comp_2_0.02_0_0.000.json  # 2 guards, 2% BW (REALISTA)
time_to_double_comp_2_0.05_0_0.000.json  # 2 guards, 5% BW
time_to_double_comp_6_0.01_0_0.000.json  # 6 guards, 1% BW
time_to_double_comp_6_0.02_0_0.000.json  # 6 guards, 2% BW
time_to_double_comp_6_0.05_0_0.000.json  # 6 guards, 5% BW (MELHOR)
```

**Formato JSON:**
```json
{
  "exp_0": [tempo_run_0, tempo_run_1, ..., tempo_run_9],
  "exp_1": [...],
  ...
  "exp_9": [...]
}
```
10 experimentos × 10 runs = **100 simulações por configuração**

---

## 🎨 `/graphs/` - Visualizações

4 gráficos gerados com `plot_results.py`:

1. **`attack_time_comparison_2020.png`**
   Box plots comparando tempos por configuração

2. **`attack_success_rate_2020.png`**
   Bar chart mostrando taxa de sucesso (%)

3. **`attack_time_heatmap_2020.png`**
   Heatmap 2D (guards × bandwidth)

4. **`paper_comparison_2020.png`**
   Comparação com resultados do paper original

**Resolução:** 300 DPI, profissional para relatórios

---

## 🔬 Como Replicar o Estudo

### 1. Download e processamento de dados:
```bash
cd 5_evaluation/study-2025

# Opção A: Download automático (se funcionar)
python3 scripts/download_consensus_2025.py

# Opção B: Download manual (mais confiável)
wget https://collector.torproject.org/recent/relay-descriptors/consensuses/consensus-2025-11-23-00-00-00 \
     -O data/consensus_2025/consensus-2025-11-23

# Processar consensus
python3 scripts/process_consensus_2025.py
```

### 2. Atualizar código de simulação:
```bash
cd ..
# Editar attack_simulation.py:
# N_HSDIRS = 5007
# RELAY_CSV = "study-2025/data/2025-11-23_relays.csv"
```

### 3. Executar simulações:
```bash
./2_script_run-simulation.sh 10 10  # 10 exp × 10 runs
```

### 4. Mover resultados:
```bash
mv time_to_double_comp_*.json study-2025/results/
```

### 5. Análise e visualização:
```bash
# Gerar estatísticas
python3 analyze_results.py

# Gerar gráficos
python3 plot_results.py
mv graphs_5_evaluation/*.png study-2025/graphs/

# Comparar com 2020
python3 study-2025/scripts/compare_2020_vs_2025.py
```

---

## 📊 Resultados-Chave

### Comparação 2020 vs 2025

| Configuração | 2020 Mediana | 2025 Mediana | Diferença | Taxa 2020 | Taxa 2025 |
|--------------|--------------|--------------|-----------|-----------|-----------|
| **2 guards, 2% BW** | 21.6s | 21.8s | **+0.2s** | 99.6% | 100% |
| **6 guards, 5% BW** | 6.7s | 6.9s | **+0.2s** | 100% | 100% |

### Crescimento da Rede vs Impacto

- **Relays:** 6451 → 9186 (+42.4%)
- **HSDirs:** 3905 → 5007 (+28.2%)
- **Impacto no ataque:** +0.8s médio (**negligenciável**)

### Conclusão

✅ **Ataque permanece altamente eficaz em 2025**
✅ **Taxa de sucesso: 85-100%** em todas as configurações
✅ **Crescimento da rede NÃO mitiga** a vulnerabilidade
⚠️ **Problema é estrutural**, requer countermeasures ativas

---

## 🔗 Ficheiros Originais do Paper (não modificados)

Estes ficheiros **não estão** em `study-2025/` porque são do estudo original:

- `2_data_attack-time/` - Resultados 2020
- `2020-09-22-18-36-48_relays.csv` - Relay list 2020
- `hsdesc_lookup_details.json` - Dados de lookup HSDir (mesmo para 2020 e 2025)
- `attack_simulation.py` - Código principal (apenas alterado N_HSDIRS e RELAY_CSV)
- `analyze_results.py` - Script de análise (reutilizado)
- `plot_results.py` - Script de visualização (reutilizado)

---

## 📝 Documentação Completa

Ver `/Notes-Trabalho-SR/5_evaluation-2025.md` para análise detalhada.

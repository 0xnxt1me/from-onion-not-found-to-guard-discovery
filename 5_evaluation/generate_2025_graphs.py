#!/usr/bin/env python3
"""
Gera gráficos específicos para dados de 2025
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configuração
DATA_DIR = Path("study-2025/results")
OUTPUT_DIR = Path("study-2025/graphs")
OUTPUT_DIR.mkdir(exist_ok=True)

configs = [
    (1, 0.01), (1, 0.02), (1, 0.05),
    (2, 0.01), (2, 0.02), (2, 0.05),
    (6, 0.01), (6, 0.02), (6, 0.05)
]

# Ler dados de 2025
medians_2025 = []
success_rates_2025 = []
labels = []

for guards, bw in configs:
    filename = DATA_DIR / f"time_to_double_comp_{guards}_{bw:.2f}_0_0.000.json"
    with open(filename) as f:
        data = json.load(f)
    
    durations = [d for d in data['attack_durations'] if d < 300]
    total = len(data['attack_durations'])
    
    if durations:
        medians_2025.append(np.median(durations))
    else:
        medians_2025.append(300)  # timeout
    
    success_rates_2025.append(len(durations) / total * 100)
    labels.append(f'{guards}g, {int(bw*100)}%')

print(f"Dados processados: {len(medians_2025)} configurações")

# ===== GRÁFICO 1: Barras de tempos 2025 =====
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(labels))
bars = ax.bar(x, medians_2025, color='#2ca02c', alpha=0.8, label='2025')

ax.set_xlabel('Configuração (Guards, Bandwidth)', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Mediano (segundos)', fontsize=12, fontweight='bold')
ax.set_title('Tempos de Ataque - Dados Novembro 2025', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Destacar cenário realista (2g, 5% = índice 5)
bars[5].set_color('#ff7f0e')
bars[5].set_alpha(1.0)

plt.tight_layout()
output_file = OUTPUT_DIR / "attack_times_2025.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Criado: {output_file}")
plt.close()

# ===== GRÁFICO 2: Heatmap 2025 =====
medians_matrix = np.array(medians_2025).reshape(3, 3)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(medians_matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=100)

ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['1%', '2%', '5%'], fontsize=11)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['1 guard', '2 guards', '6 guards'], fontsize=11)
ax.set_xlabel('Bandwidth Controlada', fontsize=12, fontweight='bold')
ax.set_ylabel('Guards Adversariais', fontsize=12, fontweight='bold')
ax.set_title('Tempo Mediano de Ataque (Novembro 2025)', fontsize=14, fontweight='bold')

# Adicionar valores nas células
for i in range(3):
    for j in range(3):
        value = medians_matrix[i, j]
        text_color = 'white' if value > 50 else 'black'
        ax.text(j, i, f'{value:.1f}s',
                ha='center', va='center', color=text_color, 
                fontsize=11, fontweight='bold')

# Destacar cenário realista (2g, 5%)
rect = plt.Rectangle((1.5, 1.5), 1, 1, fill=False, edgecolor='blue', linewidth=3)
ax.add_patch(rect)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Tempo (segundos)', rotation=270, labelpad=20, fontsize=11)

plt.tight_layout()
output_file = OUTPUT_DIR / "attack_time_heatmap_2025.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Criado: {output_file}")
plt.close()

# ===== GRÁFICO 3: Taxa de sucesso 2025 =====
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(x, success_rates_2025, color='#1f77b4', alpha=0.8)

ax.set_xlabel('Configuração (Guards, Bandwidth)', fontsize=12, fontweight='bold')
ax.set_ylabel('Taxa de Sucesso (%)', fontsize=12, fontweight='bold')
ax.set_title('Taxa de Sucesso do Ataque - Novembro 2025', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_ylim(0, 105)
ax.grid(axis='y', alpha=0.3)

# Adicionar valores
for i, (bar, rate) in enumerate(zip(bars, success_rates_2025)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{rate:.0f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
# Destacar cenário realista
bars[5].set_color('#ff7f0e')

# Linha de referência em 100%
ax.axhline(y=100, color='green', linestyle='--', linewidth=1.5, alpha=0.5, label='100% sucesso')
ax.legend(fontsize=10)

plt.tight_layout()
output_file = OUTPUT_DIR / "attack_success_rate_2025.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Criado: {output_file}")
plt.close()

# ===== GRÁFICO 4: Comparação 2020 vs 2025 lado a lado =====
# Ler dados de 2020 (dos nossos testes, não do paper)
DATA_DIR_2020 = Path(".")
medians_2020 = []

for guards, bw in configs:
    filename = DATA_DIR_2020 / f"time_to_double_comp_{guards}_{bw:.2f}_0_0.000.json"
    try:
        with open(filename) as f:
            data = json.load(f)
        durations = [d for d in data['attack_durations'] if d < 300]
        if durations:
            medians_2020.append(np.median(durations))
        else:
            medians_2020.append(300)
    except FileNotFoundError:
        medians_2020.append(0)  # Se não existir, usar 0 em vez de None

# Só criar gráfico se temos dados de 2020
if any(m > 0 for m in medians_2020):
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(labels))
    width = 0.35

    bars1 = ax.bar(x - width/2, medians_2020, width, label='2020', color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, medians_2025, width, label='2025', color='#2ca02c', alpha=0.8)

ax.set_xlabel('Configuração (Guards, Bandwidth)', fontsize=12, fontweight='bold')
ax.set_ylabel('Tempo Mediano (segundos)', fontsize=12, fontweight='bold')
ax.set_title('Comparação Temporal: 2020 vs 2025', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Destacar cenário realista
bars1[5].set_color('#ff7f0e')
bars2[5].set_color('#d62728')

    plt.tight_layout()
    output_file = OUTPUT_DIR / "comparison_2020_vs_2025.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Criado: {output_file}")
    plt.close()
else:
    print("⚠ Dados de 2020 não encontrados, gráfico de comparação não criado")

print("\n=== Resumo dos Dados 2025 ===")
print(f"Tempo mediano mínimo: {min(medians_2025):.1f}s")
print(f"Tempo mediano máximo: {max(medians_2025):.1f}s")
print(f"Taxa sucesso mínima: {min(success_rates_2025):.1f}%")
print(f"Taxa sucesso máxima: {max(success_rates_2025):.1f}%")
print(f"\nCenário realista (2g, 5%): {medians_2025[5]:.1f}s, {success_rates_2025[5]:.0f}% sucesso")
print("\nTodos os gráficos gerados com sucesso!")

#!/usr/bin/env python3
"""
Processar consenso 2025 e gerar CSV de relays similar ao de 2020
"""

import csv
from stem.descriptor import parse_file
from collections import defaultdict

consensus_file = "consensus_2025/consensus-2025-11-23"
output_csv = "2025-11-23_relays.csv"

print(f"Processando: {consensus_file}")
print()

# Parsear consenso
descriptors = parse_file(consensus_file, descriptor_type='network-status-consensus-3 1.0')

# Coletar dados dos relays
relays = []
total_bandwidth = 0
guard_bandwidth = 0
middle_bandwidth = 0
exit_bandwidth = 0

for router in descriptors:
    fingerprint = router.fingerprint
    is_guard_flag = 'Guard' in router.flags
    is_exit_flag = 'Exit' in router.flags and 'BadExit' not in router.flags
    is_hsdir = 'HSDir' in router.flags

    # Bandwidth em bytes/s
    bw = router.bandwidth
    total_bandwidth += bw

    # Classificação exclusiva seguindo a lógica do código original:
    # Prioridade: Exit > Guard > Middle
    if is_exit_flag:
        # Exit relay (não pode ser usado como guard ou middle)
        is_guard = False
        is_exit = True
        exit_bandwidth += bw
    elif is_guard_flag:
        # Guard relay (não é exit, pode ser middle também)
        is_guard = True
        is_exit = False
        guard_bandwidth += bw
        middle_bandwidth += bw
    else:
        # Middle only relay
        is_guard = False
        is_exit = False
        middle_bandwidth += bw

    relays.append({
        'nickname': router.nickname,
        'fingerprint': fingerprint,
        'is_guard': is_guard,
        'is_exit': is_exit,
        'is_hsdir': is_hsdir,
        'country': 'unknown',  # Não temos geoip no consenso básico
        'region_name': 'unknown',
        'city_name': 'unknown',
        'latitude': 0.0,
        'longitude': 0.0,
        'as': 'unknown',
        'advertised_bandwidth': bw,
    })

# Calcular probabilidades seguindo lógica do código original
for relay in relays:
    bw = relay['advertised_bandwidth']

    if relay['is_guard']:
        # Guard: tem guard_probability e middle_probability, mas NÃO exit_probability
        relay['guard_probability'] = bw / guard_bandwidth if guard_bandwidth > 0 else 0
        relay['middle_probability'] = bw / middle_bandwidth if middle_bandwidth > 0 else 0
        relay['exit_probability'] = 0.0
    elif relay['is_exit']:
        # Exit: tem exit_probability, mas NÃO guard nem middle
        relay['guard_probability'] = 0.0
        relay['middle_probability'] = 0.0
        relay['exit_probability'] = bw / exit_bandwidth if exit_bandwidth > 0 else 0
    else:
        # Middle only: tem middle_probability, mas NÃO guard nem exit
        relay['guard_probability'] = 0.0
        relay['middle_probability'] = bw / middle_bandwidth if middle_bandwidth > 0 else 0
        relay['exit_probability'] = 0.0# Escrever CSV (remover is_hsdir antes de escrever, só precisamos para estatísticas)
relays_to_write = []
for relay in relays:
    r = relay.copy()
    r.pop('is_hsdir')  # Remover campo que não está no CSV original
    relays_to_write.append(r)

with open(output_csv, 'w', newline='') as f:
    fieldnames = ['nickname', 'fingerprint', 'is_guard', 'is_exit', 'country',
                  'region_name', 'city_name', 'latitude', 'longitude', 'as',
                  'advertised_bandwidth', 'guard_probability', 'middle_probability',
                  'exit_probability']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    # Escrever cada linha formatando floats para evitar notação científica
    for relay in relays_to_write:
        # Formatar probabilidades com precisão fixa
        relay['guard_probability'] = f"{relay['guard_probability']:.15f}"
        relay['middle_probability'] = f"{relay['middle_probability']:.15f}"
        relay['exit_probability'] = f"{relay['exit_probability']:.15f}"
        writer.writerow(relay)# Estatísticas
n_total = len(relays)
n_guards = sum(1 for r in relays if r['is_guard'])
n_exits = sum(1 for r in relays if r['is_exit'])
n_hsdirs = sum(1 for r in relays if r['is_hsdir'])

print(f"Estatisticas da rede (Novembro 2025):")
print(f"  Total de relays: {n_total}")
print(f"  Guards: {n_guards} ({n_guards/n_total*100:.1f}%)")
print(f"  Exits: {n_exits} ({n_exits/n_total*100:.1f}%)")
print(f"  HSDirs: {n_hsdirs} ({n_hsdirs/n_total*100:.1f}%)")
print(f"  Total bandwidth: {total_bandwidth/1e9:.2f} GB/s")
print()
print(f"CSV gerado: {output_csv}")
print()
print("COMPARACAO com 2020:")
print(f"  2020: 6451 relays, 3905 HSDirs")
print(f"  2025: {n_total} relays, {n_hsdirs} HSDirs")
print(f"  Diferenca: {n_total-6451:+d} relays ({(n_total/6451-1)*100:+.1f}%)")
print(f"  Diferenca: {n_hsdirs-3905:+d} HSDirs ({(n_hsdirs/3905-1)*100:+.1f}%)")

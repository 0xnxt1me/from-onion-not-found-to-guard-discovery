#!/usr/bin/env python3
"""
Download consensus recente do Tor CollecTor
https://collector.torproject.org/
"""

import requests
from datetime import datetime, timedelta
import gzip
import os

# Data recente (hoje - 1 dia para garantir que existe)
target_date = datetime.now() - timedelta(days=1)
year = target_date.year
month = target_date.strftime('%m')
day = target_date.strftime('%d')

# URL do CollecTor para consensos
base_url = f"https://collector.torproject.org/archive/relay-descriptors/consensuses/consensuses-{year}-{month}.tar.xz"

print(f"A descarregar consensos de {year}-{month}...")
print(f"URL: {base_url}")
print()

# Criar pasta para dados 2025
os.makedirs("consensus_2025", exist_ok=True)

from stem.descriptor import remote

try:
    # Usar fallback directories (não requer relay específico)
    consensus = remote.get_consensus(
        timeout=60,
        fall_back_to_authority=True
    ).run()[0]

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    consensus_path = f"consensus_2025/{timestamp}-consensus"

    with open(consensus_path, 'w') as f:
        f.write(str(consensus))

    print(f"Consenso descarregado com sucesso!")
    print(f"Ficheiro: {consensus_path}")
    print()

    # Contar HSDirs
    n_hsdirs = sum(1 for _, relay in consensus.routers.items() if "HSDir" in relay.flags)
    total_relays = len(consensus.routers)

    print(f"Total de relays: {total_relays}")
    print(f"Total de HSDirs: {n_hsdirs}")
    print(f"Percentagem HSDirs: {n_hsdirs/total_relays*100:.1f}%")

except Exception as e:
    print(f"Erro ao descarregar: {e}")
    print()
    print("ALTERNATIVA: Descarregar manualmente de Tor Metrics:")
    print("https://metrics.torproject.org/networksize.html")
    print("https://collector.torproject.org/recent/relay-descriptors/consensuses/")

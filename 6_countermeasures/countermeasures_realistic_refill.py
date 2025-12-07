import sys
from attack_simulation_refill_on import run_multiple_simulations

# Customizable token bucket refill rates
# This script tests with configurable token bucket refill rates

# Usage:
#    python3 countermeasures_realistic_refill.py [vanguard_lite (0 or 1)] [both_countermeasures (0 or 1)] [refill_rate (tokens/second)]
#
# Example: 
#    python3 countermeasures_realistic_refill.py 1 1 1.0   # Both countermeasures, 60 tokens/min
#    python3 countermeasures_realistic_refill.py 1 1 0.5   # Both countermeasures, 30 tokens/min
#    python3 countermeasures_realistic_refill.py 1 1 10.0  # Both countermeasures, 600 tokens/min

if __name__ == "__main__":

    VANGUARD_LITE = False
    BOTH_COUNTERMEASURES = False
    
    N_ADV_HSDIRS = [1, 2]  # Test with h=1/6 and h=1/3
    ADV_BW_SHARE = [0.05]
    N_EXP = [10]
    N_RUNS = [10]
    N_INITIAL_TOKENS = [5, 10, 15]
    TOKEN_REFILL = [1.0]  # Default: 60 tokens/min = 1 token/second

    if len(sys.argv) >= 3:
        VANGUARD_LITE = bool(int(sys.argv[1]))
        BOTH_COUNTERMEASURES = bool(int(sys.argv[2]))
        
        # If refill rate is provided as third argument, use it
        if len(sys.argv) == 4:
            TOKEN_REFILL = [float(sys.argv[3])]
    
        if VANGUARD_LITE and not BOTH_COUNTERMEASURES:
            N_INITIAL_TOKENS = [0]

        print(f"Running simulations with:")
        print(f"  Vanguards-lite: {VANGUARD_LITE}")
        print(f"  Both countermeasures: {BOTH_COUNTERMEASURES}")
        print(f"  Token refill rate: {TOKEN_REFILL[0]} tokens/second ({TOKEN_REFILL[0]*60} tokens/min)")
        print(f"  Initial tokens: {N_INITIAL_TOKENS}")
        print(f"  HSDirs controlled: {N_ADV_HSDIRS}")
        print()

        for n_adv_hsdir in N_ADV_HSDIRS:
            for adv_bw_share in ADV_BW_SHARE:
                for n_exp in N_EXP:
                    for n_runs in N_RUNS:
                        for n_initial_tokens in N_INITIAL_TOKENS:
                            for token_ref in TOKEN_REFILL:
                                run_multiple_simulations(
                                    n_adv_hsdir,
                                    adv_bw_share,
                                    n_exp,
                                    n_runs,
                                    n_initial_tokens,
                                    token_ref,
                                    VANGUARD_LITE
                                )
    else:
        print("Usage: python3 countermeasures_realistic_refill.py [vanguard_lite (0 or 1)] [both_countermeasures (0 or 1)] [refill_rate (optional, tokens/second)]")
        print("\nExamples:")
        print("  python3 countermeasures_realistic_refill.py 1 1 1.0   # Both, 60 tokens/min")
        print("  python3 countermeasures_realistic_refill.py 1 1 0.5   # Both, 30 tokens/min")
        print("  python3 countermeasures_realistic_refill.py 1 1 10.0  # Both, 600 tokens/min")
        print("  python3 countermeasures_realistic_refill.py 1 0 2.0   # Vanguards-lite only, 120 tokens/min")

import sys
from attack_simulation_nol2guard import run_multiple_simulations

#no refill rate when both are used
#vanguard lite disables both token bucket and rate limiting
#if both countermeasures are used, token buckets do not get empty

# Usage:
#    python3 countermeasures.py [vanguard_lite (0 or 1), both_countermeasures (0 or 1)]
#
#Example: 
#    python3 countermeasures_nol2guard.py 0 0  #Buckets only
#    python3 countermeasures_nol2guard.py 1 0  #Vanguard Lite only
#    python3 countermeasures_nol2guard.py 1 1  #Both countermeasures
#

if __name__ == "__main__":

    VANGUARD_LITE = False
    BOTH_COUNTERMEASURES = False
    
    N_ADV_HSDIRS = [1,2,6]
    ADV_BW_SHARE = [0.05]
    N_EXP = [10]
    N_RUNS = [10]
    N_INITIAL_TOKENS = [5,10,15]
    TOKEN_REFILL = [0.1,0.01666]

    if len(sys.argv) == 3:
        VANGUARD_LITE = bool(int(sys.argv[1]))
        BOTH_COUNTERMEASURES = bool(int(sys.argv[2]))
    
        if VANGUARD_LITE:
            TOKEN_REFILL = [0]
            if not BOTH_COUNTERMEASURES:
                N_INITIAL_TOKENS = [0]

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
        print("\n---------------Done!---------------")

    else:
        print("Incorrect number of arguments. Usage: python countermeasures.py [vanguard_lite (0 or 1), both_countermeasures (0 or 1)]")


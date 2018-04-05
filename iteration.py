import dcgram
import yaml
import save_plot as sp

name = 'ternary_fading_channel'
load_original_sequence = False
load_machines = False
load_sequences = False
load_probabilities = False
calc_metrics = True
moore_iter = -1
save_plots = True

drange = range(4,10)    # Range of machine's memory
krange = range(4,8)     # Number of clusters for each machine with memory D
N = drange[-1] + 1      # Probabilities must be calculated for subesquences with length up to N
L = int(30e6)

for D in drange:
    if (D != drange[0]):
        load_original_sequence = False

    dcgram.DCGraM(name, load_original_sequence, load_machines, load_sequences,\
                    load_probabilities, calc_metrics, moore_iter, L, D, krange, N)
    if save_plots:
        sp.save_plot(parameter = 'cond_entropies', name = name, drange = drange,\
                        krange = krange, ylabel = '$h_{10}$')
        sp.save_plot(parameter = 'kldivergences', name = name, drange = drange,\
                        krange = krange, ylabel = '$D_{10}$')

# # ~~~~~ Moore Algorithm validation test ~~~~~
# # For D = 6, Moore takes 5 (logistic_map)
# for moore_iter in range(1,6):
#     dcgram.DCGraM(name, load_original_sequence, load_machines, load_sequences,\
#                      load_probabilities, calc_metrics, moore_iter, L, 6, krange, N)

# # ~~~~~ Moore Algorithm validation test2 ~~~~~
# for D in drange:
#     with open('../dcgram_files/{}/results/machines/dcgram/dcgram_D{}_K5.yaml'.format(name, D), 'r') as f:
#         machine = yaml.load(f)
#     K = len(machine.states)
#     dcgram.DCGraM(name, load_original_sequence, load_machines, load_sequences,\
#                      load_probabilities, calc_metrics, moore_iter, L, D, range(K, K+1), N)

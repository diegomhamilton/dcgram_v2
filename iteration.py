import dcgram

name = 'ternary_even_shift'
load_original_sequence = False
load_machines = False
load_sequences = False
load_probabilities = False
load_metrics = False
save_plots = True

drange = range(4,10)    # Range of machine's memory
krange = range(2,8)     # Number of clusters for each machine with memory D
N = drange[-1] + 1      # Probabilities must be calculated for subesquences with length up to N
L = int(10e6)

for D in drange:
    dcgram.DCGraM(name = 'logistic_map', \
                    load_original_sequence = False, \
                    load_machines = False, \
                    load_sequences = False, \
                    load_probabilities = False, \
                    load_metrics = False, \
                    save_plots = True, \
                    L = 10e6, D = D, krange = range(2,8), N = N)

## **** Plots section ****
# if save_plot:
#     plt.plot(number_of_states, sequence_entropies, 'b^-', label = 'DMarkov, D from 4 to 9')
#     #DEBUG REPORT
#     plt.plot(number_of_states_2, sequence_entropies_2, 'g^-', label = 'DCGram, D from 4 to 9')
#     plt.axhline(y=original_entropy, color='k', linestyle='-', label = 'Original sequence baseline')
#     plt.xscale('log')
#     plt.axis([1, 10000, 1.0, 1.035])
#     plt.title('Conditional entropy for the Ternary Even Shift')
#     plt.ylabel('$h_{10}$')
#     plt.xlabel('Number of states')
#     plt.legend(loc = 1)
#     plt.savefig('../dcgram_files/{}/results/plots/entropy_graph_K{}.png'.format(name, K))
#     plt.show()
#     plt.gcf().clear()
#
#     plt.plot(number_of_states, sequence_kldivergences, 'b^-', label = 'DMarkov, D from 4 to 9')
#     #DEBUG REPORT
#     plt.plot(number_of_states_2, sequence_kldivergences_2, 'g^-', label = 'DCGram, D from 4 to 9')
#     plt.xscale('log')
#     plt.axis([1, 10000, 0, 0.14])
#     plt.title('Kullback-Leibler Divergence for the Ternary Even Shift')
#     plt.ylabel('$D_{10}$')
#     plt.xlabel('Number of states')
#     plt.legend(loc = 1)
#     plt.savefig('../dcgram_files/{}/results/plots/kl_graph_K{}.png'.format(name, K))
#     plt.show()
#     plt.gcf().clear()
#
#     plt.plot(number_of_states, sequence_euclidian_distances, 'b^-', label = 'DMarkov, D from 4 to 9')
#     #DEBUG REPORT
#     plt.plot(number_of_states_2, sequence_euclidian_distances_2, 'g^-', label = 'DCGram, D from 4 to 9')
#     plt.xscale('log')
#     plt.axis([1, 10000, 0, 0.125])
#     plt.title('Euclidian Distance for the Ternary Even Shift')
#     plt.ylabel('$d_{10}$')
#     plt.xlabel('Number of states')
#     plt.legend(loc = 1)
#     plt.savefig('../dcgram_files/{}/results/plots/euclidian_graph_K{}.png'.format(name, K))
#     plt.show()
#     plt.gcf().clear()

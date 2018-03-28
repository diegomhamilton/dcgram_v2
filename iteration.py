import dcgram
import yaml

''' Correct:
        python3 iteration.py
Traceback (most recent call last):
  File "iteration.py", line 25, in <module>
    load_probabilities, load_metrics, save_plots, L, D, krange, N)
  File "/home/sid/workspace/IC/dcgram_v2/dcgram.py", line 65, in DCGraM
    dcgram_machines[K-1] = km.clusterize(dmark_machines, L, D, K, name = name)
  File "/home/sid/workspace/IC/dcgram_v2/kmeans.py", line 66, in clusterize
    new_pt = final_pt.redefine_partition()
  File "/home/sid/workspace/IC/dcgram_v2/partitionset.py", line 68, in redefine_partition
    probs = np.mean(curr_probs)
  File "/home/sid/anaconda3/lib/python3.6/site-packages/numpy/core/fromnumeric.py", line 2909, in mean
    out=out, **kwargs)
  File "/home/sid/anaconda3/lib/python3.6/site-packages/numpy/core/_methods.py", line 70, in _mean
    ret = umr_sum(arr, axis, dtype, out, keepdims)
TypeError: cannot perform reduce with flexible type

'''

name = 'logistic_map'
load_original_sequence = False
load_machines = False
load_sequences = False
load_probabilities = False
calc_metrics = True
moore_iter = 0
save_plots = True

drange = range(4,10)    # Range of machine's memory
krange = range(3,4)     # Number of clusters for each machine with memory D
N = drange[-1] + 1      # Probabilities must be calculated for subesquences with length up to N
L = int(10e6)

# # ~~~~~ Moore Algorithm validation test ~~~~~
# # For D = 6, Moore takes 5 (logistic_map)
# for moore_iter in range(1,6):
#     dcgram.DCGraM(name, load_original_sequence, load_machines, load_sequences,\
#                      load_probabilities, calc_metrics, moore_iter, L, 6, krange, N)

# # ~~~~~ Moore Algorithm validation test2 ~~~~~
for D in drange:
    with open('../dcgram_files/{}/results/machines/dcgram/dcgram_D{}_K5.yaml'.format(name, D), 'r') as f:
        machine = yaml.load(f)
    K = len(machine.states)
    dcgram.DCGraM(name, load_original_sequence, load_machines, load_sequences,\
                     load_probabilities, calc_metrics, moore_iter, L, D, range(K, K+1), N)


# ~~~~~~~~ UNCOMMENT ~~~~~~~~~~~~~
# for D in drange:
#     dcgram.DCGraM(name, load_original_sequence, load_machines, load_sequences,\
#                     load_probabilities, calc_metrics, moore_iter, L, D, krange, N)
#     if save_plots:
#         sp.save_plot(parameter = 'cond_entropies', name = name, drange = drange,\
#                         krange = krange, ylabel = '$h_{10}$')
#         sp.save_plot(parameter = 'kldivergences', name = name, drange = drange,\
#                         krange = krange, ylabel = '$D_{10}$')


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

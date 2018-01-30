import yaml
import sequenceanalyzer as sa
import sequence_generator as sg
import dmarkov as dm
import matplotlib.pyplot as plt

name = 'ternary_even_shift'
load_original_sequence = False
load_machines = True
load_sequences = False
load_probabilities = False
save_plot = False

drange = range(4,10)# User defined range of machine's memory
N = drange[-1] + 1  # Probabilities must be calculated for subesquences with length up to N
L = int(10e6)

if load_original_sequence:
    # Load original sequence
    with open('../dcgram_files/{}/sequences/original_v1.yaml'.format(name), 'r') as f:
        original_sequence = yaml.load(f)

# Load sequence alphabet
with open('../dcgram_files/{}/alphabet.yaml'.format(name), 'r') as f:
    alphabet = yaml.load(f)
# Load original sequence probabilities
with open('../dcgram_files/{}/results/probabilities/original_v1.yaml'.format(name),\
'r') as f:
    original_probs = yaml.load(f)
# Load original sequence conditional probabilities
with open('../dcgram_files/{}/results/probabilities/conditional/original_v1\
.yaml'.format(name), 'r') as f:
    original_cond_probs = yaml.load(f)

# Machine intialization section
dmark_machines = [None]*drange[-1]
#DEBUG REPORT
dcgram_machines = [None]*drange[-1]

if load_machines:
    # Load previously generated DMarkov Machines for D in drange
    for D in drange:
        with open('../dcgram_files/{}/results/machines/dmark_{}.yaml'.format(name, D), \
        'r') as f:
            dmark_machines[D-1] = yaml.load(f)
        #DEBUG REPORT
        with open('../dcgram_files/{}/results/machines/dcgram_{}.yaml'.format(name, D), \
        'r') as f:
            dcgram_machines[D-1] = yaml.load(f)
else:
    # Generate DMarkov Machines for D in drange
    for D in drange:
        dmark_machines[D-1] = dm.DMarkov(original_cond_probs, D, alphabet)

        with open('../dcgram_files/{}/results/machines/dmark_{}.yaml'.format(name, D), \
        'w') as f:
            yaml.dump(dmark_machines[D-1], f)

dmark_probs = [None] * D
dmark_cond_probs = [None] * D
#DEBUG REPORT
dcgram_probs = [None] * D
dcgram_cond_probs = [None] * D

# Sequence generation and/or probabilities initialization
if not load_probabilities:
    # Sequences initialization section
    dmark_sequences = [None] * D

    if load_sequences:
        # Load existing sequences
        for D in drange:
            with open('../dcgram_files/{}/results/sequences/dmark_{}.yaml'.format(name, D), \
            'r') as f:
                dmark_sequences[D-1] = yaml.load(f)
    else:
        for D in drange:
            dmark_sequences[D-1] = sg.generate_sequence(dmark_machines[D-1], D, L)   \

            with open('../dcgram_files/{}/results/sequences/dmark_{}.yaml'.format(name, D), \
            'w') as f:
                yaml.dump(dmark_sequences[D-1], f)

            # Computes probabilities
            dmark_probs[D-1], alphabet = sa.calc_probs(dmark_sequences[D-1], N)
            # Saves probabilities
            with open('../dcgram_files/{}/results/probabilities/dmark_{}.yaml'.format(name, D),\
             'w') as f:
                yaml.dump(dmark_probs[D-1], f)
            # Computes conditional probabilities
            dmark_cond_probs[D-1] = sa.calc_cond_probs(dmark_probs[D-1], alphabet, N-1)
            # Saves conditional probabilities
            with open('../dcgram_files/{}/results/probabilities/conditional/dmark_{}.yaml'\
            .format(name, D), 'w') as f:
               yaml.dump(dmark_cond_probs[D-1], f)
else:
    for D in drange:
        with open('../dcgram_files/{}/results/probabilities/dmark_{}.yaml'.format(name, D),\
         'r') as f:
            dmark_probs[D-1] = yaml.load(f)
        with open('../dcgram_files/{}/results/probabilities/conditional/dmark_{}.yaml'\
        .format(name, D), 'r') as f:
            dmark_cond_probs[D-1] = yaml.load(f)
        #DEBUG REPORT
        with open('../dcgram_files/{}/results/probabilities/dcgram_{}.yaml'.format(name, D),\
         'r') as f:
            dcgram_probs[D-1] = yaml.load(f)
        with open('../dcgram_files/{}/results/probabilities/conditional/dcgram_{}.yaml'\
        .format(name, D), 'r') as f:
            dcgram_cond_probs[D-1] = yaml.load(f)

# Data analysis section

number_of_states = []
sequence_entropies = []
sequence_kldivergences = []
sequence_euclidian_distances = []

for D in drange:
    curr_machine = dmark_machines[D-1]
    curr_probs = dmark_probs[D-1]
    curr_cond_probs = dmark_cond_probs[D-1]

    number_of_states.append(len(curr_machine.states))
    sequence_entropies.append(sa.calc_cond_entropy(curr_probs, curr_cond_probs, 9)[-1])
    sequence_kldivergences.append(sa.calc_kldivergence(curr_probs, original_probs, 10))
    sequence_euclidian_distances.append(sa.calc_euclidian_distance(curr_probs, original_probs, 10))

#DEBUG REPORT
number_of_states_2 = []
sequence_entropies_2 = []
sequence_kldivergences_2 = []
sequence_euclidian_distances_2 = []
for D in drange:
    curr_machine = dcgram_machines[D-1]
    curr_probs = dcgram_probs[D-1]
    curr_cond_probs = dcgram_cond_probs[D-1]

    number_of_states_2.append(len(curr_machine.partitions))
    sequence_entropies_2.append(sa.calc_cond_entropy(curr_probs, curr_cond_probs, 9)[-1])
    sequence_kldivergences_2.append(sa.calc_kldivergence(curr_probs, original_probs, 10))
    sequence_euclidian_distances_2.append(sa.calc_euclidian_distance(curr_probs, original_probs, 10))

# Plots section
if save_plot:
    plt.plot(number_of_states, sequence_entropies, 'b^-')
    #DEBUG REPORT
    plt.plot(number_of_states_2, sequence_entropies_2, 'g^-')
    plt.xscale('log')
    plt.axis([0.1, 10000, 1.0, 1.035])
    plt.savefig('../dcgram_files/{}/results/plots/entropy_graph.png'.format(name))
    plt.show()
    plt.gcf().clear()

    plt.plot(number_of_states, sequence_kldivergences, 'b^-')
    #DEBUG REPORT
    plt.plot(number_of_states_2, sequence_kldivergences_2, 'g^-')
    plt.xscale('log')
    plt.axis([0.1, 10000, 0, 0.14])
    plt.savefig('../dcgram_files/{}/results/plots/kl_graph.png'.format(name))
    plt.show()
    plt.gcf().clear()

    plt.plot(number_of_states, sequence_euclidian_distances, 'b^-')
    #DEBUG REPORT
    plt.plot(number_of_states_2, sequence_euclidian_distances_2, 'g^-')
    plt.xscale('log')
    plt.axis([0.1, 10000, 0, 0.2])
    plt.savefig('../dcgram_files/{}/results/plots/euclidian_graph.png'.format(name))
    plt.show()
    plt.gcf().clear()

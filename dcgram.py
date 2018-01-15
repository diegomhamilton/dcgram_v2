import yaml
import sequenceanalyzer as sa
import sequence_generator as sg
import dmarkov as dm
import matplotlib.pyplot as plt

load_original_sequence = False
load_machines = True
load_sequences = False
load_probabilities = True
save_plot = True

drange = range(4,10)# User defined range of machine's memory
N = drange[-1] + 1  # Probabilities must be calculated for subesquences with length up to N
L = int(10e7)

if load_original_sequence:
    # Load original sequence
    with open('ternary_even_shift/sequences/original_v1\
    .yaml', 'r') as f:
        original_sequence = yaml.load(f)

# Load sequence alphabet
with open('ternary_even_shift/alphabet.yaml', 'r') as f:
    alphabet = yaml.load(f)
# Load original sequence probabilities
with open('ternary_even_shift/results/probabilities/original_v1\
.yaml', 'r') as f:
    original_probs = yaml.load(f)
# Load original sequence conditional probabilities
with open('ternary_even_shift/results/probabilities/conditional/original_v1\
.yaml', 'r') as f:
    original_cond_probs = yaml.load(f)

# Machine intialization section
dmark_machines = [None]*drange[-1]

if load_machines:
    # Load previously generated DMarkov Machines for D in drange
    for D in drange:
        with open('ternary_even_shift/results/machines/dmark_{}.yaml'.format(D), \
        'r') as f:
            dmark_machines[D-1] = yaml.load(f)
else:
    # Generate DMarkov Machines for D in drange
    for D in drange:
        dmark_machines[D-1] = dm.DMarkov(original_cond_probs, D, alphabet)

        with open('ternary_even_shift/results/machines/dmark_{}.yaml'.format(D), \
        'w') as f:
            yaml.dump(dmark_machines[D-1], f)

dmark_probs = [None] * D
dmark_cond_probs = [None] * D

# Sequence generation and/or probabilities initialization
if not load_probabilities:
    # Sequences initialization section
    dmark_sequences = [None] * D

    if load_sequences:
        # Load existing sequences
        for D in drange:
            with open('ternary_even_shift/results/sequences/dmark_{}.yaml'.format(D), \
            'r') as f:
                dmark_sequences[D-1] = yaml.load(f)
    else:
        for D in drange:
            dmark_sequences[D-1] = sg.generate_sequence(dmark_machines[D-1], D, L)   \

            with open('ternary_even_shift/results/sequences/dmark_{}.yaml'.format(D), \
            'w') as f:
                yaml.dump(dmark_sequences[D-1], f)

            # Computes probabilities
            dmark_probs[D-1], alphabet = sa.calc_probs(dmark_sequences[D-1], N)
            # Saves probabilities
            with open('ternary_even_shift/results/probabilities/dmark_{}.yaml'.format(D),\
             'w') as f:
                yaml.dump(dmark_probs[D-1], f)
            # Computes conditional probabilities
            dmark_cond_probs[D-1] = sa.calc_cond_probs(dmark_probs[D-1], alphabet, N-1)
            # Saves conditional probabilities
            with open('ternary_even_shift/results/probabilities/conditional/dmark_{}.yaml'\
            .format(D), 'w') as f:
               yaml.dump(dmark_cond_probs[D-1], f)
else:
    for D in drange:
        with open('ternary_even_shift/results/probabilities/dmark_{}.yaml'.format(D),\
         'r') as f:
            dmark_probs[D-1] = yaml.load(f)
        with open('ternary_even_shift/results/probabilities/conditional/dmark_{}.yaml'\
        .format(D), 'r') as f:
            dmark_cond_probs[D-1] = yaml.load(f)

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

# Plots section
if save_plot:
    plt.plot(number_of_states, sequence_entropies, 'ro')
    plt.xscale('log')
    plt.axis([0.1,10000,1.0,1.035])
    plt.savefig('ternary_even_shift/results/plots/entropy_graph.png')
    plt.show()
    plt.gcf().clear()

    plt.plot(number_of_states, sequence_kldivergences, 'bx')
    plt.xscale('log')
    plt.axis([0.0,10000,0,0.14])
    plt.savefig('ternary_even_shift/results/plots/kl_graph.png')
    plt.show()
    plt.gcf().clear()

    plt.plot(number_of_states, sequence_euclidian_distances, 'g^')
    plt.xscale('log')
    plt.axis([0.0,10000, 0, 1.0])
    plt.savefig('ternary_even_shift/results/plots/euclidian_graph.png')
    plt.show()
    plt.gcf().clear()

import kmeans
import yaml
import sequenceanalyzer as sa

name = 'ternary_even_shift'
drange = range(4,10)
N = drange[-1] + 1
L = int(10e6)

dcgram_probs = [None] * drange[-1]
dcgram_cond_probs = [None] * drange[-1]

for D in drange:
    sequence = kmeans.save_sequence(D, L)

    with open('../dcgram_files/{}/results/sequences/dcgram_{}.yaml'.format(name, D), 'w') as f:
        yaml.dump(sequence, f)

    # Computes probabilities
    dcgram_probs[D-1], alphabet = sa.calc_probs(sequence, N)
    # Saves probabilities
    with open('../dcgram_files/{}/results/probabilities/dcgram_{}.yaml'.format(name, D),\
     'w') as f:
        yaml.dump(dcgram_probs[D-1], f)
    # Computes conditional probabilities
    dcgram_cond_probs[D-1] = sa.calc_cond_probs(dcgram_probs[D-1], alphabet, N-1)
    # Saves conditional probabilities
    with open('../dcgram_files/{}/results/probabilities/conditional/dcgram_{}.yaml'\
    .format(name, D), 'w') as f:
       yaml.dump(dcgram_cond_probs[D-1], f)

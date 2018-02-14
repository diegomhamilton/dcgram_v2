import yaml
import sequenceanalyzer as sa
import sequence_generator as sg
import dmarkov as dm
import matplotlib.pyplot as plt
import kmeans as km

def DCGraM(name = 'ternary_even_shift', \
            load_original_sequence = True, \
            load_machines = False, \
            load_sequences = False, \
            load_probabilities = False, \
            load_metrics = False, \
            save_plots = True, \
            L = 10e6, D = 4, krange = range(2,8), N = 10):

    # **** Sequence initialization section ****
    if load_original_sequence:
        # Load original sequence
        with open('../dcgram_files/{}/original/original_v1.yaml'.format(name), 'r') as f:
            original_sequence = yaml.load(f)
        # Calculate probabilities
        original_probs, alphabet = sa.calc_probs(original_sequence, N)
        with open('../dcgram_files/{}/original/alphabet.yaml'.format(name), 'w') as f:
            yaml.dump(alphabet, f)
        with open('../dcgram_files/{}/results/probabilities/original_v1.yaml'.format(name),\
        'w') as f:
            yaml.dump(original_probs, f)
        original_cond_probs = sa.calc_cond_probs(original_probs, alphabet, N-1)
        with open('../dcgram_files/{}/results/probabilities/conditional/original_v1\
                .yaml'.format(name), 'w') as f:
            yaml.dump(original_cond_probs, f)
    else:
        # Load sequence alphabet
        with open('../dcgram_files/{}/original/alphabet.yaml'.format(name), 'r') as f:
            alphabet = yaml.load(f)
        # Load original sequence probabilities
        with open('../dcgram_files/{}/results/probabilities/original_v1.yaml'.format(name),\
        'r') as f:
            original_probs = yaml.load(f)
        # Load original sequence conditional probabilities
        with open('../dcgram_files/{}/results/probabilities/conditional/original_v1\
                .yaml'.format(name), 'r') as f:
            original_cond_probs = yaml.load(f)

    # **** Machine initialization section ****
    dcgram_machines = [None]*krange[-1]

    if load_machines:
        # Load previously generated DMarkov Machines for D in drange
        with open('../dcgram_files/{}/results/machines/dmarkov/dmark_{}.yaml'.format(name, D), \
        'r') as f:
            dmark_machines = yaml.load(f)
        for K in krange:
            with open('../dcgram_files/{}/results/machines/dcgram/dcgram_D{}_K{}.yaml'.format(name, D, K), \
            'r') as f:
                dcgram_machines[K-1] = yaml.load(f)
    else:
        # Generate DMarkov Machines for D in drange
        dmark_machines = dm.DMarkov(original_cond_probs, D, alphabet)
        with open('../dcgram_files/{}/results/machines/dmarkov/dmark_{}.yaml'.format(name, D), \
        'w') as f:
            yaml.dump(dmark_machines, f)
        for K in krange:
            dcgram_machines[K-1] = km.clusterize(dmark_machines[D-1], L, D, K, name = name)

    dcgram_sequences = [[None] * K for d in drange]
    dmark_cond_probs = [None] * K
    dcgram_cond_probs = [None] * K

    # **** Sequence generation and/or probabilities initialization ****
    if not load_probabilities:
        if load_sequences:
            # Load existing sequences
            with open('../dcgram_files/{}/results/sequences/dmarkov/dmark_{}.yaml'.format(name, D), \
            'r') as f:
                dmark_sequences = yaml.load(f)
            for K in krange:
                with open('../dcgram_files/{}/results/sequences/dcgram/dcgram_D{}_K{}.yaml'\
                            .format(name, D, K), 'r') as f:
                    dmark_sequences[K-1] = yaml.load(f)
        else:
            dmark_sequences[D-1] = sg.generate_sequence(dmark_machines[D-1], L)
            with open('../dcgram_files/{}/results/sequences/dmarkov/dmark_{}.yaml'\
                        .format(name, D), 'w') as f:
                yaml.dump(dmark_sequences[D-1], f)
            for K in krange:
                dcgram_sequences[K-1] = sg.generate_sequence(dcgram_machines[K-1], L)
                with open('../dcgram_files/{}/results/sequences/dcgram/dcgram_D{}_K{}.yaml'\
                            .format(name, D, K), 'w') as f:
                    yaml.dump(dcgram_sequences[K-1], f)

            # Computes probabilities
            dmark_probs, alphabet = sa.calc_probs(dmark_sequences[D-1], N)
            # Saves probabilities
            with open('../dcgram_files/{}/results/probabilities/dmarkov/dmark_{}.yaml'.format(name, D),\
             'w') as f:
                yaml.dump(dmark_probs, f)
            # Computes conditional probabilities
            dmark_cond_probs[D-1] = sa.calc_cond_probs(dmark_probs[D-1], alphabet, N-1)
            # Saves conditional probabilities
            with open('../dcgram_files/{}/results/probabilities/conditional/dmarkov/dmark_{}.yaml'\
            .format(name, D), 'w') as f:
               yaml.dump(dmark_cond_probs[D-1], f)
            with open('../dcgram_files/{}/results/probabilities/conditional/dcgram/dcgram_D{}_K{}.yaml'\
            .format(name, D, K), 'w') as f:
                 yaml.dump(dcgram_cond_probs[D-1], f)

            for K in krange:
                # Computes probabilities
                dcgram_probs[K-1], alphabet = sa.calc_probs(sequence, N)
                # Saves probabilities
                with open('../dcgram_files/{}/results/probabilities/dcgram/dcgram_D{}_K{}.yaml'\
                            .format(name, D, K), 'w') as f:
                    yaml.dump(dcgram_probs[K-1], f)
                # Computes conditional probabilities
                dcgram_cond_probs[K-1] = sa.calc_cond_probs(dcgram_probs[D-1], alphabet, N-1)
                # Saves conditional probabilities
                with open('../dcgram_files/{}/results/probabilities/conditional/dcgram/dcgram_D{}_K{}.yaml'\
                            .format(name, D, K), 'w') as f:
                    yaml.dump(dcgram_cond_probs[K-1], f)
    else:
        with open('../dcgram_files/{}/results/probabilities/dmarkov/dmark_{}.yaml'.format(name, D),\
         'r') as f:
            dmark_probs = yaml.load(f)
        with open('../dcgram_files/{}/results/probabilities/conditional/dmarkov/dmark_{}.yaml'\
        .format(name, D), 'r') as f:
            dmark_cond_probs = yaml.load(f)

        for K in krange:
            with open('../dcgram_files/{}/results/probabilities/dcgram/dcgram_D{}_K{}.yaml'.format(name, D, K),\
             'r') as f:
                dcgram_probs[K-1] = yaml.load(f)
            with open('../dcgram_files/{}/results/probabilities/conditional/dcgram/dcgram_D{}_K{}.yaml'\
            .format(name, D, K), 'r') as f:
                dcgram_cond_probs[K-1] = yaml.load(f)

    # **** Data analysis section ****
    original_entropy = sa.calc_cond_entropy(original_probs, original_cond_probs, 9)[-1]

    with open('../dcgram_files/{}/results/cond_entropies/original_v1.yaml'\
                .format(name), 'w') as f:
        yaml.dump(original_entropy, f)

    dmark_entropy = sa.calc_cond_entropy(dcgram_probs, dmark_cond_probs, 9)[-1]
    with open('../dcgram_files/{}/results/cond_entropies/dmarkov/dmark_D{}.yaml'\
                .format(name, D), 'w') as f:
        yaml.dump(dmark_entropy, f)
    dmark_kldiv = sa.calc_kldivergence(dmark_probs, original_probs, 10)
    with open('../dcgram_files/{}/results/kldivergences/dmarkov/dmark_D{}.yaml'\
                .format(name, D), 'w') as f:
        yaml.dump(dmark_kldiv, f)
    # dmark_edist = sa.calc_euclidian_distance(dmark_probs, original_probs, 10)
    # with open('../dcgram_files/{}/results/euclidiandistance/dmarkov/dmark_D{}.yaml'\
    #             .format(name, D), 'w') as f:
    #     yaml.dump(dmark_edist, f)

    dcgram_entropy = []
    dcgram_kldiv = []
    # dcgram_edist = []
    for K in drange:
        curr_machine = dcgram_machines[K-1]
        curr_probs = dcgram_probs[K-1]
        curr_cond_probs = dcgram_cond_probs[K-1]

        dcgram_entropy.append(sa.calc_cond_entropy(curr_probs, curr_cond_probs, 9)[-1])
        with open('../dcgram_files/{}/results/cond_entropies/dcgram/dcgram_D{}_K{}.yaml'\
                    .format(name, D, K), 'w') as f:
            yaml.dump(dcgram_entropy, f)
        dcgram_kldiv.append(sa.calc_kldivergence(curr_probs, original_probs, 10))
        with open('../dcgram_files/{}/results/kldivergences/dcgram/dcgram_D{}_K{}.yaml'\
                    .format(name, D, K), 'w') as f:
            yaml.dump(original_entropy, f)
        # dcgram_edist.append(sa.calc_euclidian_distance(curr_probs, original_probs, 10))
        # with open('../dcgram_files/{}/results/euclidiandistance/dcgram/dcgram_D{}_K{}.yaml'\
        #             .format(name, D, K), 'w') as f:
        #     yaml.dump(original_entropy, f)

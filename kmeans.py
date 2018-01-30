import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as k
import dmarkov as dmkv
import yaml
import partition as pt
import partitionset as ps
import moore as m
import numpy as np
import random


def save_sequence(D, L=10e7, model = 'ternary_even_shift'):
    with open('../dcgram_files/{}/results/machines/dmark_{}.yaml'.format(model, D), 'r') as f:
         machine = yaml.load(f)

    all_oedges = [state.outedges for state in machine.states]
    morphs = []

    for oedges in all_oedges:
        curr_morph = [0, 0, 0]
        for oedge in oedges:
            label = oedge[0]
            curr_morph[int(label)] = oedge[-1]
        morphs.append(curr_morph)

    kmeans = k(n_clusters = 3, random_state = 0).fit(morphs)

    clusters = [[] for i in range(kmeans.n_clusters)]

    for i in range(len(morphs)):
        clusters[kmeans.labels_[i]].append(morphs[i])

    idx = 0
    plot = ['bo','g*','c^', 'mo', 'y*', 'k^', 'ro']
    for c in clusters:
        plt.plot([x[0] for x in c], [y[1] for y in c], plot[idx])
        idx += 1

    plt.plot([x[0] for x in kmeans.cluster_centers_], [y[1] for y in kmeans.cluster_centers_], 'r+')
    plt.savefig('../dcgram_files/ternary_even_shift/results/plots/kmeans_dmark_7_3_clusters.png')
    #----------------------------------------------------------------------------------
    #MOORE
    clusters = [[] for i in range(kmeans.n_clusters)]

    for i in range(len(morphs)):
        clusters[kmeans.labels_[i]].append(machine.states[i])

    initial_partition = []

    for p in clusters:
        partition = pt.Partition()
        for state in p:
            partition.add_to_partition(state)
        initial_partition.append(partition)


    initial_partition = ps.PartitionSet(initial_partition)
    final_partition = m.moore(initial_partition, machine)

    for p in final_partition.partitions:
        for i in range(len(p.name)):
            print('name:{}|oedge:{}'.format(p.name[i],p.outedges[i]))
        print('--------------\n')

    # class kmeans(KMeans):
    #     def __init__(self, machine, n, r):
    #         morphs = self.get_morphs(machine)
    #
    #         super().__init__(self, n_clusters = n, random_state = r\
    #         ).fit(morphs)
    #
    #     def get_morphs(self, machine):
    #         '''doc'''
    #         all_oedges = [state.outedges for state in machine.states]
    #         morphs = []
    #
    #         for oedges in all_oedges:
    #             curr_morph = [0, 0, 0]
    #
    #             for oedge in oedges:
    #                 label = oedge[0]
    #                 curr_morph[int(label)] = oedge[-1]
    #             morphs.append(curr_morph)
    #         return morphs

    #?
    #BEGINNING
    avg_morphs = []

    for p in final_partition.partitions:
        morphs = []

        for oedges in p.outedges:
            curr_morph = [0, 0, 0]
            for oedge in oedges:
                label = oedge[0]
                curr_morph[int(label)] = oedge[-1]
            morphs.append(curr_morph)

        means = []

        for i in range(len(curr_morph)):
            means.append(np.mean([m[i] for m in morphs]))

        avg_morphs.append(means)
    # END

    #PUT ON sequencegenerator.py
    #BEGINNING
    sequence = ''
    curr_partition = 0

    for i in range(L):
        # Set data parameters
        labels = [str(label) for label in range(len(avg_morphs[curr_partition]))]
        probabilities = avg_morphs[curr_partition]
        # Weight formatting
        for weight in probabilities:
            weight = int(weight * 10e16)
        # Chooses next state
        label = random.choices(labels, probabilities)[0]
        sequence = sequence + label
        #CREATE FUNCTION ON partitionset.py CALLED find_next_partition
        #BEGINNING
        for oedge in (final_partition.partitions[curr_partition]).outedges[0]:
            if oedge[0] == label:
                state = oedge[1] #name of next state (gets first outedge in partition)
        #DEBUG
        print(state)
        j = 0
        breaker = False
        for p in final_partition.partitions:
            for state_named in p.name:
                if state_named == state:
                    curr_partition = j
                    #DEBUG
                    print(final_partition.partitions[curr_partition].name)
                    breaker = True
                    break
            if breaker:
                break
            else:
                j += 1
        print()
        #END
    #END
    return sequence

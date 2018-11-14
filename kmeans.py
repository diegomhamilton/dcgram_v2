import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as k
import dmarkov as dmkv
import yaml
import partition as pt
import partitionset as ps
import moore as m
import numpy as np
import random
import sequence_generator as sg


def clusterize(machine, L, D, K, moore_iter = -1, \
                name = 'ternary_even_shift', save_plot = True):
    all_oedges = [state.outedges for state in machine.states]
    morphs = []
    # define label for files if not default Moore's algorithm execution
    if moore_iter != -1:
        moore_label = '_moore_{}_iter'.format(moore_iter)
    else:
        moore_label = ''

    # Normalize morphs
    for oedges in all_oedges:
        curr_morph = [0] * len(machine.index_labels)
        for oedge in oedges:
            label = oedge[0]
            curr_morph[machine.index_labels[label]] = oedge[-1]
        morphs.append(curr_morph)
    # print('Morphs:\n{}'.format(morphs))
    kmeans = k(n_clusters = K, random_state = 0).fit(morphs)
    clusters = [[] for i in range(kmeans.n_clusters)]
    for i in range(len(morphs)):
        clusters[kmeans.labels_[i]].append(morphs[i])
    if save_plot:
        idx = 0
        plot_label = ['bo','g*','c^', 'ms', 'yp', 'kh', 'rd', 'b>', 'r<']*5
        for c in clusters:
            plt.plot([x[0] for x in c], [y[1] for y in c], plot_label[idx], alpha = 0.7)
            idx += 1

        plt.plot([x[0] for x in kmeans.cluster_centers_], [y[1] for y in kmeans.cluster_centers_], 'r+', markersize = 15)
        plt.axis([-0.05, 1.05, -0.05, 1.05])
        # plt.title('Agrupamento de morphs para D = {}, K = {}'.format(D, K))
        plt.ylabel('$P(0)$')
        plt.xlabel('$P(1)$')
        plt.savefig(f'../dcgram_files/{name}/results/plots/kmeans_dmark_D{D}_K{K}_clusters{moore_label}.png')
        plt.gcf().clear()
    #----------------------------------------------------------------------------------
    #MOORE
    clusters = [[] for i in range(kmeans.n_clusters)]
    # print(f"Clusterization check")
    for i in range(len(morphs)):
        state_idx = kmeans.labels_[i]
        # print(f"\tCenter: {kmeans.cluster_centers_[state_idx]}, Outedge: {machine.states[i].outedges}")
        clusters[kmeans.labels_[i]].append(machine.states[i])
    # Fix empty clusters problem
    clusters = [c for c in clusters if c]

    initial_pt = []

    for p in clusters:
        partition = pt.Partition()
        for state in p:
            partition.add_to_partition(state)
        initial_pt.append(partition)

    initial_pt = ps.PartitionSet(initial_pt)
    final_pt = m.moore_by_parts(machine, initial_pt, n_iter = moore_iter)

    with open(f'../dcgram_files/{name}/results/machines/dcgram/before_redefine/dcgram_D{D}_K{K}{moore_label}.yaml', 'w') as f:
        yaml.dump(final_pt, f)
    new_pt = final_pt.redefine_partition(machine)

    with open(f'../dcgram_files/{name}/results/machines/dcgram/dcgram_D{D}_K{K}{moore_label}.yaml'\
                , 'w') as f:
        yaml.dump(new_pt, f)

    return new_pt

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

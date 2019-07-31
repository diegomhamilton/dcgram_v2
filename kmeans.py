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
import eigenvectorcalcs as eig

def dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b), axis=1)

# def dist(a, b):
#     eps = 1e-15
#     a = np.array(a, dtype='float64')
#     b = np.array(b, dtype='float64')
#     a[a == 0] = eps
#     b[b == 0] = eps
#     kl = (a*np.log(a/b) + b*np.log(b/a))/2
    
#     if a.shape != b.shape:
#         return np.sum(kl, axis = 0)
#     if a.shape == b.shape:
#         return np.sum(kl, axis = 1)

##def dist(vec1, vec2):
##    kl = [0, 0]
##    print("Calculating Kullback-Leibler divergence")
##    if len(vec1) and len(vec1) == len(vec2):
##        #Probabilities of subsequences of length K are stored in probabilities[K-1]
##        for i in range(len(vec1)):
##            p = vec1[i] or 1e-15
##            q = vec2[i] or 1e-15
##            # print(f'p={p}, q={q}')
##            kl[0] += p*np.log2(p/q)
##            kl[1] += p*np.log2(p/q)
##    else:
##        print ("[error] Probabilities not computed.")
##    print("*****************")
##    print("Kullback-Leibler divergence calculated!")
##    print("*****************")
##    return (kl[0]+kl[1])/2

def custom_kmeans(matrix, k, centroids, weights):
    current_centroids = np.array(centroids)
    matrix = np.array(matrix)
    weights = np.array(weights)
    previous_centroids = np.zeros(current_centroids.shape)

    error = dist(current_centroids, previous_centroids)
    nearest_clusters = np.zeros(len(matrix))
    # print('~~~ Starting K-Means ~~~')
    while sum(error) > 0.01:
        # print(f'Error = {sum(error)}')
        for i in range(len(matrix)):
            distances = dist(matrix[i], current_centroids)
            nearest_clusters[i] = np.argmin(distances)
            # print(f'Distance to centroids : {distances}\n Nearest_cluster: {nearest_clusters[i]}\n')

            previous_centroids = current_centroids.copy()

        for i in range(k):
            current_centroids[i] = np.average(matrix[np.where(nearest_clusters == i)], axis=0, weights=weights[np.where(nearest_clusters == i)])
        print(f'New centroids: {current_centroids}\n Old centroids: {previous_centroids}\n\n')

        error = dist(current_centroids, previous_centroids)
    return (nearest_clusters, current_centroids)

def get_initial_centroids(samples = [], K = 5):
    i = 0
    centroids = []

    for sample in samples:
        if sample not in centroids:
            centroids.append(sample)
            i += 1
        if i == K:
            return np.array(centroids)
    return []

def clusterize(machine, L, D, K, moore_iter = -1, label_length = 1, machine_original = None, \
                name = 'ternary_even_shift', save_plot = True, version = 'v1'):
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
    centers = get_initial_centroids(morphs, K)
    closest_cluster, kmeans_centers = custom_kmeans(morphs, K, centers, machine.state_prob)
    closest_cluster = [int(i) for i in closest_cluster]
    clusters = [[] for i in closest_cluster]
    for i in range(len(morphs)):
        clusters[closest_cluster[i]].append(morphs[i])
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
        plt.savefig(f'../dcgram_files/{name}_{version}/results/plots/kmeans_dmark_D{D}_K{K}_clusters{moore_label}_n{label_length}.png')
        plt.gcf().clear()
    #----------------------------------------------------------------------------------
    #MOORE
    clusters = [[] for i in closest_cluster]
    # print(f"Clusterization check")
    for i in range(len(morphs)):
        cluster_index = closest_cluster[i]
        # print(f"\tCenter: {kmeans.cluster_centers_[state_idx]}, Outedge: {machine.states[i].outedges}")
        clusters[cluster_index].append(machine_original.states[i])
    # Fix empty clusters problem
    clusters = [c for c in clusters if c]
    # Split cluster if two or more states have differente outedges

    new_clusters = []

    for c in clusters:
        new_clusters_dict = dict()
        for st in c:
            key = ''.join([oedge[0] for oedge in st.outedges])
            if key in new_clusters_dict:
                new_clusters_dict[key].append(st)
            else:
                new_clusters_dict[key] = [st]
        for new_c in new_clusters_dict.values():
            new_clusters.append(new_c)
 
    initial_pt = []

    for p in new_clusters:
        partition = pt.Partition()
        for state in p:
            partition.add_to_partition(state)
        initial_pt.append(partition)

    initial_pt = ps.PartitionSet(initial_pt)

    with open(f'../dcgram_files/{name}_{version}/results/machines/dcgram/before_redefine/initial_D{D}_K{K}{moore_label}_n{label_length}.yaml', 'w') as f:
        yaml.dump(initial_pt, f)
        
    final_pt = m.moore_by_parts(machine_original, initial_pt, n_iter = moore_iter)

    with open(f'../dcgram_files/{name}_{version}/results/machines/dcgram/before_redefine/dcgram_D{D}_K{K}{moore_label}_n{label_length}.yaml', 'w') as f:
        yaml.dump(final_pt, f)
    new_pt = final_pt.redefine_partition(machine_original)

    with open(f'../dcgram_files/{name}_{version}/results/machines/dcgram/dcgram_D{D}_K{K}{moore_label}_n{label_length}.yaml'\
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

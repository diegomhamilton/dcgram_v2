import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as k
import dmarkov as dmkv
import yaml
import partition as pt
import partitionset as ps
import moore as m

with open('../dcgram_files/ternary_even_shift/results/machines/dmark_6.yaml', 'r') as f:
     machine = yaml.load(f)

all_oedges = [state.outedges for state in machine.states]
morphs = []

for oedges in all_oedges:
    curr_morph = [0, 0, 0]
    for oedge in oedges:
        label = oedge[0]
        curr_morph[int(label)] = oedge[-1]
    morphs.append(curr_morph)

kmeans = k(n_clusters = 6, random_state = 0).fit(morphs)

clusters = [[] for i in range(kmeans.n_clusters)]

for i in range(len(morphs)):
    clusters[kmeans.labels_[i]].append(morphs[i])

idx = 0
plot = ['bo','g*','c^', 'mo', 'y*', 'k^']
for c in clusters:
    plt.plot([x[0] for x in c], [y[1] for y in c], plot[idx])
    idx += 1

plt.plot([x[0] for x in kmeans.cluster_centers_], [y[1] for y in kmeans.cluster_centers_], 'r+')
plt.savefig('../dcgram_files/ternary_even_shift/results/plots/kmeans_dmark_6_6_clusters.png')
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

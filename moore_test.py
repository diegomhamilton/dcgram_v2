import yaml
import partition as pt
import partitionset as ps
import moore as m
from sklearn.cluster import KMeans as k

with open('../dcgram_files/ternary_even_shift/results/machines/dmarkov/dmark_D6.yaml', 'r') as f:
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
    clusters[kmeans.labels_[i]].append(machine.states[i])
initial_pt = []

for p in clusters:
    partition = pt.Partition()
    for state in p:
        partition.add_to_partition(state)
    initial_pt.append(partition)

initial_pt = ps.PartitionSet(initial_pt, alphabet = ['0', '1', '2'])
final_pt = m.moore_by_parts(machine, initial_pt, n_iter = 3)

def save_machine(D=3, K=5, n=1):
     with open(f'../dcgram_files/logistic_map_v1/results/machines/dcgram/before_redefine/initial_D{D}_K{K}_n{n}.yaml', 'r') as f:
             m = yaml.load(f)
     with open(f'./machines_after_kmeans/D{D}_K{K}_n{n}.txt', 'w') as f:
     	     for p in m.partitions:
                 f.write(f'{p.name}\n')
                 for o in p.outedges:
                         f.write(f'\t{o}\n')
                 f.write('\n')

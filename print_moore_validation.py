import yaml

drange = range(4,10)

for D in drange:
     with open('../dcgram_files/logistic_map/results/machines/dcgram/dcgram_D{}_K5.yaml'.format(D), 'r') as f:
             K = len((yaml.load(f)).states)
     with open('../dcgram_files/logistic_map/results/cond_entropies/dcgram/dcgram_D{}_K{}_moore_0_iter.yaml'.format(D,K), 'r') as f:
             print('Conditional entropy for D={}, K={} (DCGraM): {}'.format(D, K, yaml.load(f)))
     with open('../dcgram_files/logistic_map/results/cond_entropies/dmarkov/dmark_D{}.yaml'.format(D), 'r') as f:
             print('Conditional entropy for D={} (DMarkov): {}'.format(D, yaml.load(f)))
     print()
     with open('../dcgram_files/logistic_map/results/kldivergences/dcgram/dcgram_D{}_K{}_moore_0_iter.yaml'.format(D,K), 'r') as f:
             print('Kullback-Leibler Divergence for D={}, K={} (DCGraM): {}'.format(D, K, yaml.load(f)))
     with open('../dcgram_files/logistic_map/results/kldivergences/dmarkov/dmark_D{}.yaml'.format(D), 'r') as f:
             print('Kullback-Leibler Divergence for D={} (DMarkov): {}'.format(D,yaml.load(f)))
     print()
     print()

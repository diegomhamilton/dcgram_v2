import sys
sys.path.insert(0, '../')

import yaml
import sequenceanalyzer as sa

with open('../../dcgram_files/logistic_map/results/machines/dcgram/dcgram_D4_n1_K5.yaml', 'r') as f:
    m = yaml.load(f)
with open('../../dcgram_files/logistic_map/results/sequences/dcgram/dcgram_D4_n1_K5.yaml', 'r') as f:
    s = yaml.load(f)
with open('../../dcgram_files/logistic_map/original/original_len_10000000.yaml', 'r') as f:
    s_ori = yaml.load(f)

print('dcgram:')
oc_test = sa.calc_occup_vector(m, s, 1000)
print('\n\noriginal:')
oc_ori = sa.calc_occup_vector(m, s_ori, 10000)


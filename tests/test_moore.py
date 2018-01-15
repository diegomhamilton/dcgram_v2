import yaml
import partition as pt
import partitionset as ps
import moore as m

with open('../results/ternary_even_shift/results/machines/dmark_4.yaml', 'r') as f:
    machine = yaml.load(f)

with open('tests/pt_test.yaml', 'r') as f:
    init_pt = yaml.load(f)

final_pt = m.moore(init_pt, machine)

for p in final_pt.partitions:
    print('----------PARTITION--------------')
    for i in range(len(p.name))
        print(p.name[i])
        print(p.outedges[i])
        print()

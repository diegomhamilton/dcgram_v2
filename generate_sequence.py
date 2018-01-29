import numpy as np
import random

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

for i in range(100):
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

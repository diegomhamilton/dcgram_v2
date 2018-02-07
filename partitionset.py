import partition
import graph as gr
import probabilisticgraph as pg
import state as st
import probabilisticstate as pst
import random
import numpy as np

'''
A Partition Set is a collection of partition, which, in turn are collections
of states which share some common feature. From a deterministic partition set
it is possible to recover a graph.
'''


class PartitionSet:
    def __init__(self, partitions):
        self.partitions = partitions

    # Not in current use:
    # def update_partitions_edges(self):
    #    for part in self.partitions:
    #        for other in self.partitions:
    #            part.update_edges(other)
    '''
    Name: find_in_partition
    Input:
        *name: name of the state to be found
    Output:
        *idx: index of the partition that contains the state
    '''
    def find_in_partition(self, name):
        idx = 0
        for p in self.partitions:
            if name in p.name:
                return idx
            else:
                idx += 1
        idx = -1
        return idx
    '''
    Name: redefine_partition
    Output:
        *new_graph: probabilistic graph with partition redefined as states
    Description:
        Redefines partition name as their index in the PartitionSet, choosing
    randomly an destination state (in case the same label leads to different
    partitions) and calculates the average probabilities for each edge.
    '''
    def redefine_partition(self):
        new_states = [pst.ProbabilisticState(name = i) for i in range(len(self.partitions))]
        alphabet = set([])

        for s in new_states:
            all_oedges = self.partitions[s.name].outedges
            random_oedges = random.choice(all_oedges)

            new_oedges = []
            i = 0
            for oedge in random_oedges:
                label = oedge[0]
                alphabet.add(label)
                dest = self.find_in_partition(oedge[1])
                curr_probs = [morph[i][-1] for morph in all_oedges]
                probs = np.mean(curr_probs)
                i += 1
                new_oedges.append((label, dest, probs))
            s.outedges = new_oedges

        return new_states

    '''
    Name: recover_graph
    Input:
        *g: original graph that generated this partition set
    Output:
        *h: graph created by making the partition set into a graph
    Description:
    '''

    def recover_graph(self, g, base_probs=None):
        new_states = []
        for p in self.partitions:
            s = g.state_named(p.name[0])
            oedge = []
            for a in g.alphabet:
                t = s.next_state_from_edge(a)
                if t:
                    for p in self.partitions:
                        if t.name in p.name:
                            dest = p.name[0]
                            break
                        else:
                            dest = ''
                else:
                    dest = ''
                for e in s.outedges:
                    if e[0] == a:
                        newedge = []
                        i = 0
                        for element in e:
                            if i == 1:
                                # The outedges are created pointing just
                                # to a name, not to a state:
                                newedge.append(dest)
                            else:
                                newedge.append(element)
                            i += 1
                        if base_probs:
                            avg = self.average_probs(base_probs, p, g, a)
                            newedge.append(avg)
                        newedge = tuple(newedge)
                        oedge.append(newedge)
            u = st.State(s.name, oedge)
            new_states.append(u)
        h = gr.Graph(new_states, g.alphabet)
        return h

    def average_probs(self, base_probs, p, g, a):
        probs = {}
        for nm in p.name:
            lng = len(nm) - 1
            d = base_probs[lng]
            probs[nm] = d[nm]
        total_prob = sum(probs.values())
        prob_for_edge = []
        p_outedges = {n:g.state_named(n).outedges for n in p.name}
        for nm in p.name:
            outedges = p_outedges[nm]
            for edge in outedges:
                if edge[0] == a:
                    val = edge[2]*probs[nm]
                    break
            prob_for_edge.append(val)
        avg = sum(prob_for_edge)/total_prob
        return avg

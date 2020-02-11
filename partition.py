from probabilisticstate import ProbabilisticState

class Partition(ProbabilisticState):
    '''
    A partition is a state created by merging states together after it is
    computed they represent an equivalent state. It has the same attributes as
    the class State, but it includes functions that add new states to the
    partition and that updates its outedges to the names of another partition
    of the same partition set.
    '''

    def __init__(self, state=None):
        #A new partition is initialized with just one state:
        self.name = [] if not state else [state.name]
        self.outedges = [] if not state else [state.outedges]
        self.state_probs = [] if not state else [state.state_prob]
        self.size = 0 if not state else 1

    def add_to_partition(self, state):
        '''
        Input: state to be added to the partition
        Output: the current partition will now have a new state
        '''

        #Checks to see whether the state is already in the partition:
        if state.name not in self.name:
            self.name.append(state.name)
            #Adds each outedge of the added state to the partition's edges:
            self.outedges.append(state.outedges)
            self.state_probs.append(state.state_prob)
            self.size += 1

    def remove_from_partition(self, name):
        idx = self.name.index(name)
        if idx >= 0:
            self.name.remove(self.name[idx])
            self.outedges.remove(self.outedges[idx])

    def update_edges(self, partition):
        '''
        Input: partition to which the edges should be updated.
        Output: the current partition will have its outedges update accordingly.
        Description: When a partition has a new state added to it, all the
        partitions that had that state in its outedges have to update the
        outedges in order to include the whole new partition at its destination
        state.
        '''
        #Checks if the destination state is included in the input partition's
        #name. If it is, outedges is updated: the destination state receives the
        #input partition's name.
        i = 0
        for edge in self.outedges:
            if edge[1] in partition.name:
                new_edge = (self.outedges[0], partition.name)
                if new_edge not in self.outedges:
                    self.outedges[i] = edge
                else:
                    self.outedges.remove(self.outedges[i])
            i += 1

    # returns all outedges completed with outedges that have p = 0
    def fill_outedges(self, machine):
        new_oedges = []
        label_names = machine.label_names
        index_labels = machine.index_labels

        for oedge in self.outedges:
            new_e = [None] * len(index_labels)
            for label in label_names:
                new_e[index_labels[label]] = (label, -1, 0.0)
            for e in oedge:
                new_e[index_labels[e[0]]] = e
            new_oedges.append(new_e)
        return new_oedges
    
    def __str__(self):
        for i in range(0, len(self.name)):
            print(f'{self.name[i]}: {self.outedges[i]}')

        return 'end of partition\r\n'
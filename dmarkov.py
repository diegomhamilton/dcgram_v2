import probabilisticgraph as pg
import probabilisticstate as pst
import itertools

'''
This class creates a probabilistic graph from a rooted tree with probabilities
g. It takes its states with length D, extracts them and connects them in a 
D-Markov fashion, creating a new graph.
'''
class DMarkov(pg.ProbabilisticGraph):
    def __init__(self, p_cond, D, alphabet = [], label_size = 1):
        p_curr = p_cond[D] #Conditional probabilities of length D words
        #Generates all possible state names with length D from alphabet letters
        state_names = [''.join(i) for i in itertools.product(alphabet, repeat = D)]
        self.label_names = [''.join(i) for i in itertools.product(alphabet, repeat = label_size)]
        #Creates a dictionary of type label_name: index for faster index access
        self.label_names.sort()
        self.index_labels = {}
        i = 0
        for w in self.label_names:
            self.index_labels[w] = i
            i += 1
        d_states = []
        for name in state_names:
            outedges = []
            for a in self.label_names:
                dest = name[label_size:] + a
                key = a + '|' + name
                if key in p_curr.keys() and p_curr[key] != 0:
                    prob = p_curr[a + '|' + name]
                    outedges.append((a, dest, prob))
                
            #Append states if exists outedge (state not stranded)
            if outedges:
                d_states.append(pst.ProbabilisticState(name, outedges))
    
        pg.ProbabilisticGraph.__init__(self, d_states, alphabet)
        
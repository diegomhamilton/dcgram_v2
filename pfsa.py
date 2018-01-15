'''
This file implements a PFSA class that is used in the D-Markov and DCGraM algorithms.
The PFSA consists of a pandas table and a list containing the PFSA alphabet.
Each row of the table represents one state of the PFSA. 
The state has a column for its label and a pair of columns for each symbol in the alphabet.
For a given symbol s in the alphabet, the column s contains the label to which the state transitions with the symbol s.
The column P(s) contains the probability with each it transitions with symbol s.
Besides that, this class contains methods related to the PFSA, such as sequence generation.
'''
import pandas as pd
import numpy.random as rd

class PFSA():
    def __init__(self, path_states='', path_alph='', states='', alphabet=''):
        if path_states:
            self.states = pd.read_csv(path_states)
        else:
            self.states = states
            
        if path_alph:
            self.alphabet = pd.read_csv(path_alph)
        else:
            self.alphabet = alphabet
            
    def generate_sequence(self, length, init_state=0):
        seq = ''
        curr_state = self.states[init_state, :]
        for i in range(N):
            sym = rd.choice(self.alphabet, self.get_morph(curr_state))
            seq += sym
            next_state_label = curr_state[[sym]]
            curr_state = self.states.loc[next_state_label]
        return seq
            
    def get_morph(self, state):
        col_filter = [col for col in list(state) if col.startswith('P')]
        morph = state[col_filter]
        return morph
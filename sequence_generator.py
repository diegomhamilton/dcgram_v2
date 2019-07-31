import numpy as np
import dmarkov as dmkv
import random
from timeit import default_timer as timer

'''
Name: generate_sequence
Input:
    *machine: DMarkov machine from which the sequence will be created.
    *D: memory of the machine.
    *L: sequence size.
Output:
    *sequence: sequence with size L obtained from machine with memory D.
Description:
    Starts with an predetermined state (all zeroes) and iterates L times,
    choosing next state in accord with labels probabilities.
'''
def generate_sequence(machine, L, label_size = 1):
    sequence = ''
    # Starts in machine's first state
    curr_state_name = machine.states[0].name

    for state in machine.states:
        if (state.name == curr_state_name):
            curr_state = state

    #Generate a L length sequence from DMarkov with D = curr_d
    for i in range(int(L/label_size)):
        # Set data parameters
        labels = [outedge[0] for outedge in curr_state.outedges]
        probabilities = [outedge[-1] for outedge in curr_state.outedges]
        # Weight formatting
        probabilities = [int(p * 10e16) for p in probabilities]
        # Chooses next state
        label = random.choices(labels, probabilities)[0]
        # print(f'Labe = {label}')
        sequence = sequence + label
        # Goes to next state
        curr_state_name = [outedge[1] for outedge in curr_state.outedges if \
                            outedge[0] == label][0]
        for state in machine.states:
            if (state.name == curr_state_name):
                curr_state = state
    return sequence


# thinking machine as a dict {state: outedge}
def generate_sequence_and_occup_vector(machine, L):
    sequence = ''
    states = machine.states
    curr_state = states[0]
    idx = dict((s.name, states.index(s)) for s in states)
    st_counter = np.zeros(len(states))

    for i in range(int(L)):
        # Set data parameters
        labels = [outedge[0] for outedge in curr_state.outedges]
        probabilities = [outedge[-1] for outedge in curr_state.outedges]
        # Weight formatting
        probabilities = [int(p * 10e16) for p in probabilities]
        # Chooses next state
        label = random.choices(labels, probabilities)[0]
        sequence += label
        # Goes to next state
        next_state_name = [outedge[1] for outedge in curr_state.outedges if \
                            outedge[0] == label][0]
        curr_state = states[idx[next_state_name]]

        st_counter[idx[curr_state.name]] += 1
    
    occup_vector = st_counter/st_counter.sum()

    return sequence, occup_vector

def logistic_map(x0 = 0.5, r = 3.75):
     x = [x0]
     s = ''
     for i in range(10000000):
             x.append(r*x[i]*(1-x[i]))
             if x[i] <= 0.67:
                     s += '0'
             elif x[i] <= 0.79:
                     s += '1'
             else:
                     s += '2'
     return s
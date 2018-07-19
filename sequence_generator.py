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
    for i in range(L/label_size):
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
def generate_sequence_dict(machine, L):
    sequence = ''
    # Starts in machine's first state
    curr_state_name = list(machine.keys())[0]

    #Generate a L length sequence from DMarkov with D = curr_d
    for i in range(L):
        # Set data parameters
        labels = [oedge[0] for oedge in machine[curr_state_name]]
        probabilities = [oedge[-1] for oedge in machine[curr_state_name]]
        # Weight formatting
        probabilities = [int(p * 10e16) for p in probabilities]
        # Chooses next state
        label = random.choices(labels, probabilities)[0]
        # print(f'Label = {label}')
        sequence = sequence + label
        # Goes to next state
        curr_state_name = [oedge[1] for oedge in machine[curr_state_name] if oedge[0] == label[0]][0]
    return sequence

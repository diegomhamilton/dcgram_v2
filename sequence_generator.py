import numpy as np
import dmarkov as dmkv
import random

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
def generate_sequence(machine, L):
    sequence = ''
    # Starts in machine's first state
    curr_state_name = machine.states[0].name

    for state in machine.states:
        if (state.name == curr_state_name):
            curr_state = state

    #Generate a 10e7 length sequence from DMarkov with D = curr_d
    for i in range(L):
        # Set data parameters
        labels = [outedge[0] for outedge in curr_state.outedges]
        probabilities = [outedge[-1] for outedge in curr_state.outedges]
        # Weight formatting
        for weight in probabilities:
            weight = int(weight * 10e16)
        # Chooses next state
        label = random.choices(labels, probabilities)[0]
        sequence = sequence + label
        # Goes to next state
        curr_state_name = [outedge[1] for outedge in curr_state.outedges if \
                            outedge[0] == label][0]
        for state in machine.states:
            if (state.name == curr_state_name):
                curr_state = state

    return sequence

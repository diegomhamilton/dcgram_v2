import numpy as np
from scipy.linalg import eig

def near(a, b, rtol = 1e-5, atol = 1e-8):
    return np.abs(a-b)<(atol+rtol*np.abs(b))

def trans_prob_matrix(machine):
    n = len(machine.states)
    P = np.zeros((n, n))
    st_names = [st.name for st in machine.states]
    idxs = {k: v for v, k in enumerate(st_names)}
    
    for st in machine.states:
        cur_st = idxs[st.name]
        for oedg in st.outedges:
            next_st = idxs[oedg[1]]
            P[cur_st][next_st] += oedg[-1]
    return P

def occup_vector(machine):
    P = trans_prob_matrix(machine)
    values, vectors = eig(P, right = False, left = True)
    vectors = np.matrix.transpose(vectors)
    return vectors[near(values, 1)][0]

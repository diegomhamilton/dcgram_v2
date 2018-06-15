import numpy as np
import pandas as pd
#debug
from timeit import default_timer as timer

def calc_probs(X, L):
    print(f'Calculating probabilities for words with length {L} ...')
    probabilities = []
    alphabet = set([c for c in X]) # computes all differents characters in sequence 
    max_probs = {}
    init_time = timer()
    for i in range(0, len(X) - L):
        curr_word = ''.join(map(str, X[i:(i+L)]))
        if not curr_word in max_probs.keys():
            max_probs[curr_word] = 1
        else:
            max_probs[curr_word] += 1
    for key in max_probs.keys():
        # max_probs[key] /= float(len(X))
        max_probs[key] /= float(len(X) - (L-1))
    probabilities.insert(0, max_probs)

    for l in range(L, 1, -1):
        print(f'Calculating probabilities for words with length {l-1} ...')
        node_prob = {}
        aux_probs = max_probs.copy()
            
        for key in max_probs.keys():
            sub_word = key[0:-1]
            sub_prob = aux_probs.pop(key, 0)
            # print(f'word:{key}; curr_prob:{sub_prob}')
            for c in alphabet:
                comp_word = sub_word + str(c)
                sub_prob += aux_probs.pop(comp_word, 0)
                # print(f'\tword:{comp_word}; curr_prob:{sub_prob}')
            # print(f'\tsub_word:{sub_word}')
            if not sub_word in node_prob.keys():
                node_prob[sub_word] = sub_prob
        # print(node_prob)
        probabilities.insert(0, node_prob)
        max_probs = node_prob.copy()
    # print(f'took {timer()-init_time} secs')
    return [probabilities, alphabet]


'''
Name: calc_probs
Input:
    *X: sequence to be analyzed
    *L: maximum sub-sequence length to be analyzed.
Output:
    *probabilities: a list of dictionaries. Each dictionary contains keys
     that are sequences of the same length. The value associated to a key
     is a probability of that subsequence appearing in the original sequence
    *alphabet: the unique symbols that appear in the sequence.
Description:
    Checks the number of occurances of subsequences of lengths from 1 to L.
    Divides the number of occurances by the sequence's length in order to
    obtain relative frequencies. Creates a dictionary for subsequences of
    each length. When checking for subsequences of length 1, the method
    records each individual symbol that appears and stores it as the
    sequence's alphabet.
'''
def old_calc_probs(X, L):
    #Output lists, initialized as empty lists:
    probabilities = []
    alphabet = []
    print("Calculating subsequence probabilities")
    print("L = " + str(L))
    init_time = timer()
    #This first loop iterates the subsequence length to be analyzed:
    for l in range(1, L + 1):
        print("Calculating probabilities of subsequences of length: " + str(l))
        current_probs = {} #Dictionary storing the probabilities of current l
        #This loop traverses the string counting occurences of subsequences:
        for i in range(0, len(X) - (l - 1)):
            #current_value stores a string with the subsequence from position
            #i to position i+l
            current_value = ''.join(str(e) for e in X[i:i+l])
            #When l is 1, the unique symbols are stored in alphabet:
            if l == 1:
                if not (current_value in alphabet):
                    alphabet.append(current_value)
            #If the key for current_value has not appeared yet, it is created
            #and its count starts at 1.
            if not current_value in current_probs.keys():
                current_probs[current_value] = 1
            #If the key has already shown up, its count is incremented.
            else:
                current_probs[current_value] += 1
        #After the sequence is analyzed, the counts for each key are divided by
        #the sequence's length in order to get probabilities:
        for key in current_probs.keys():
            current_probs[key] /= float(len(X))
        probabilities.append(current_probs)
    print("*****************")
    print("Probabilities calculated!")
    print("*****************")

    print(f'took {timer()-init_time} secs')
    return [probabilities, alphabet]

'''
Name: calc_cond_probs
Input:
    *L: maximum sub-sequence length to be analyzed.
Output:
    *conditional_probabilities: a list of dictionaries. Each dictionary
     contains keys that are of the form:
     symbol|subsequence
     meaning the probability of "symbol" occuring after that subsequence.
     There is one dictionary for each length of subsequence.
Description:
    Calculates the probability of each symbol in alphabet occuring each
    subsequence in probabilities and create a similiar dictionary for those
    conditional probabilities.
'''
def calc_cond_probs(probabilities, alphabet, L):
    #Output initialized as empty list:
    conditional_probabilities = []
    print("Calculating subsequence conditional probabilities")
    print("L = " + str(L))
    if probabilities:
        #The first element, i.e. the probabilities of each symbol given the
        #empty string is just the probabilities of the occurence of those
        #symbols, i.e. the first element of the probabilities list.
        conditional_probabilities = [probabilities[0]]
        #This loop calculates the conditional probabilities of subsquences of
        #length greater than 0 given each symbol in the alphabet:
        for l in range(0, L-1):
            print("Calculating conditional probabilities of subsequences of length: " + str(l+1))
            d = {}
            l1 = probabilities[l]
            l2 = probabilities[l+1]
            for s in l1:
                for a in alphabet:
                    cond = a + "|" + s
                    t = s + a
                    if t in l2.keys():
                        d[cond] = l2[t]/l1[s]
                    else:
                        d[cond] = 0.0
            conditional_probabilities.append(d)
    else:
        print("Probabilities not computed.")
        print("Run calc_probs function before this one.")
    print("*****************")
    print("Conditional probabilities calculated!")
    print("*****************")
    return conditional_probabilities

def calc_cond_entropy(probabilities, conditional_probabilities, L):
        cond_entropy = []
        print("Calculating conditional entropy for sequence at: ")
        print("L = " + str(L))
        if probabilities:
            if conditional_probabilities:
                for l in range(0, L):
                    #l means the number of conditional bits. So for a fixed l, we calculate  h_{l+1}.
                    # print("Sequence: ")
                    # print("Calculating conditional entropy of length: " + str(l+1))
                    acc = 0
                    p = probabilities[l]
                    pcond = conditional_probabilities[l]
                    for x in p.keys():
                        # print('x=' + x)
                        if l == 0:
                            acc -= p[x]*np.log2(p[x])
                        else:
                            y_given_x = x[-1] + '|' + x[0:-1]
                            if not pcond[y_given_x] == 0:
                                acc -= p[x]*np.log2(pcond[y_given_x])
                    cond_entropy.append(acc)
            else:
                print("Conditional probabilities not computed.")
                print("Run calc_cond_probs function before this one.")
        else:
            print("Probabilities not computed.")
            print("Run calc_probs function before this one.")
        print("*****************")
        print("Sequence: ")
        print("Conditional entropy calculated!")
        print("*****************")
        return cond_entropy


'''
Name: calc_kldivergence
Input:
    *base_probs: A list of probability dictionaries to which the
        probabilities contained in this class will be compared.
    *K: The length/level of probabilities from each that will be compared.
Output:
    *kldivergence: The Kullback-Leibler Divergence between the probability
        distributions of sequences of length K from base_probs and
        probabilities.
Description:
    Calculates the KL Divergence of prob distributions of K-length seqs.
'''
def calc_kldivergence(seq_probs, base_probs, K):
    kldivergence = 0
    print("Calculating Kullback-Leibler divergence for sequence at: ")
    print("K = " + str(K))
    if seq_probs:
        #Probabilities of subsequences of length K are stored in probabilities[K-1]
        for key in base_probs[K-1].keys():
            p = base_probs[K-1][key]
            if key in seq_probs[K-1].keys():
                q = seq_probs[K-1][key]

                if not q:
                    q = 1e-15
            else:
                q = 1e-15 #Default non-zero really small value

            kldivergence += p*np.log2(p/q)
    else:
        print ("[error] Probabilities not computed.")
        print("Run calc_probs function before this one.")
    print("*****************")
    print("Sequence test: ")
    print("Kullback-Leibler divergence calculated!")
    print("*****************")
    return kldivergence

def calc_euclidian_distance(seq_probs, base_probs, K):
    euclidian_distance = 0
    print('Calculating Euclidian Distance for sequence at: ')
    print('K={}'.format(K))

    if seq_probs:
        #Probabilities of subsequences of length K are stored in probabilities[K-1]
        for key in base_probs[K-1].keys():
            p = base_probs[K-1][key]
            if key in seq_probs[K-1].keys():
                q = seq_probs[K-1][key]

                if not q:
                    q = 0
            else:
                q = 0 #Default non-zero really small value

            euclidian_distance += abs(p - q)
    else:
        print ("[error] Probabilities not computed.")
        print("Run calc_probs function before this one.")
    print("*****************")
    print("Sequence test: ")
    print("Euclidian Distance calculated!")
    print("*****************")
    return euclidian_distance

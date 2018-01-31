import os

path = '../dcgram_files'

def organize_folders(sequence, version = 'v1'):
    subfolders = ['sequences', 'machines', 'probabilities', 'probabilities/conditional', 'cond_entropies', 'kldivergences', 'plots']

    if not os.path.exists('{}/{}/original'.format(path, sequence)):
        os.makedirs('{}/{}/original'.format(path, sequence))

    new_path = '{}/{}/results'.format(path, sequence)
    for f in subfolders:
        if not os.path.exists('{}/{}/dcgram'.format(new_path, f)):
            os.makedirs('{}/{}/dcgram'.format(new_path, f))
        if not os.path.exists('{}/{}/dmarkov'.format(new_path, f)):
            os.makedirs('{}/{}/dmarkov'.format(new_path, f)) 

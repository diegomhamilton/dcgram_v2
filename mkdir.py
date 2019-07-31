import os

global_path = '../dcgram_files'

def organize_folders(sequence, version = 'v1', path_dir = ''):
    subfolders = ['sequences', 'machines', 'probabilities', 'probabilities/conditional', 'cond_entropies', 'kldivergences', 'plots']
    if path_dir:
        path = path_dir
    else:
        path = global_path
        
    if not os.path.exists('{}/{}_{}/original'.format(path, sequence, version)):
        os.makedirs('{}/{}_{}/original'.format(path, sequence, version))

    new_path = '{}/{}_{}/results'.format(path, sequence, version)
    for f in subfolders:
        if not os.path.exists('{}/{}/dcgram'.format(new_path, f)):
            os.makedirs('{}/{}/dcgram'.format(new_path, f))
        if not os.path.exists('{}/{}/dmarkov'.format(new_path, f)):
            os.makedirs('{}/{}/dmarkov'.format(new_path, f))

    if not os.path.exists('{}/machines/dcgram/before_redefine'.format(new_path)):
        os.makedirs(f'{new_path}/machines/dcgram/before_redefine')

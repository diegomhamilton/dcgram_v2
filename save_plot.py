import yaml
import matplotlib.pyplot as plt

def save_plot(parameter = 'cond_entropies', name = 'ternary_even_shift', version = 'v1',\
                drange = range(4,10), krange = range(2,8), moore_iter = -1, label_length = 1, title = 'Insert your title here', xlabel = 'Number of states', ylabel = ''):
    dcgram_parameters = [[None] * len(drange) for i in range(krange[-1])]
    dcgram_states = [[None] * len(drange) for i in range(krange[-1])]
    dmark_parameters = [None] * len(drange)
    dmark_states = [None] * len(drange)

    if moore_iter != -1:
        moore_label = f'_moore_{moore_iter}_iter'
    else:
        moore_label = ''

    for D in drange:
        with open(f'../dcgram_files/{name}_{version}/results/{parameter}/dmarkov/dmark_D{D}.yaml', 'r') as f:
            dmark_parameters.append(yaml.load(f))
        with open(f'../dcgram_files/{name}_{version}/results/machines/dmarkov/dmark_D{D}.yaml', 'r') as f:
            machine = yaml.load(f)
            dmark_states.append(len(machine.states))

        for K in krange:
            with open(f'../dcgram_files/{name}_{version}/results/{parameter}/dcgram/dcgram_D{D}_K{K}{moore_label}_n{label_length}.yaml', 'r') as f:
                dcgram_parameters[K-1].append(yaml.load(f))
            with open(f'../dcgram_files/{name}_{version}/results/machines/dcgram/dcgram_D{D}_K{K}{moore_label}_n{label_length}.yaml', 'r') as f:
                machine = yaml.load(f)
                dcgram_states[K-1].append(len(machine.states))
    plt.plot(dmark_states, dmark_parameters, 'g^-', label = f'D-Markov, D de {drange[0]} a {drange[-1]}', linewidth = 1.0)
    if parameter == 'cond_entropies':
        with open(f'../dcgram_files/{name}_{version}/results/{parameter}/original_v1.yaml', 'r') as f:
            original_parameter = yaml.load(f)
        plt.axhline(y=original_parameter, color='k', linestyle='-', label = 'Sequência original')
    else:
        plt.axhline(y=0, color='k', linestyle='-', linewidth = 1.0)
    plt.xscale('log')
    idx = 0
    plot_label = ['b^-', 'c+-', 'm*-', 'y^-', 'k^-', 'r^-']
    for K in krange:
        plt.plot(dcgram_states[K-1], dcgram_parameters[K-1], plot_label[idx], label = f'DCGraM, D de {drange[0]} a {drange[-1]}, K={K}'.format(K), linewidth = 1.0, alpha = 0.65)
        idx += 1
    # plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 1)
    plt.show()

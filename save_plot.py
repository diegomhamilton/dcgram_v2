import yaml
import matplotlib.pyplot as plt

def save_plot(parameter = 'cond_entropies', name = 'ternary_even_shift',\
                drange = range(4,10), krange = range(2,8), moore_iter = -1, title = 'Insert your title here', xlabel = 'Number of states', ylabel = ''):
    dcgram_parameters = [[None] * len(drange) for i in range(krange[-1])]
    dcgram_states = [[None] * len(drange) for i in range(krange[-1])]
    dmark_parameters = [None] * len(drange)
    dmark_states = [None] * len(drange)

    if moore_iter != -1:
        moore_label = f'_moore_{moore_iter}_iter'
    else:
        moore_label = ''

    for D in drange:
        with open('../dcgram_files/{}/results/{}/dmarkov/dmark_D{}.yaml'.format(name, parameter, D), 'r') as f:
            dmark_parameters.append(yaml.load(f))
        with open('../dcgram_files/{}/results/machines/dmarkov/dmark_D{}.yaml'.format(name, D), 'r') as f:
            machine = yaml.load(f)
            dmark_states.append(len(machine.states))

        for K in krange:
            with open('../dcgram_files/{}/results/{}/dcgram/dcgram_D{}_K{}{}.yaml'.format(name, parameter, D, K, moore_label), 'r') as f:
                dcgram_parameters[K-1].append(yaml.load(f))
            with open('../dcgram_files/{}/results/machines/dcgram/dcgram_D{}_K{}{}.yaml'.format(name, D, K, moore_label), 'r') as f:
                machine = yaml.load(f)
                dcgram_states[K-1].append(len(machine.states))
    plt.plot(dmark_states, dmark_parameters, 'g^-', label = 'D-Markov, D de 4 a 9', linewidth = 1.0)
    if parameter == 'cond_entropies':
        with open('../dcgram_files/{}/results/{}/original_v1.yaml'.format(name, parameter), 'r') as f:
            original_parameter = yaml.load(f)
        plt.axhline(y=original_parameter, color='k', linestyle='-', label = 'Sequência original')
    else:
        plt.axhline(y=0, color='k', linestyle='-', linewidth = 1.0)
    plt.xscale('log')
    idx = 0
    plot_label = ['b^-', 'c+-', 'm*-', 'y^-', 'k^-', 'r^-']
    for K in krange:
        plt.plot(dcgram_states[K-1], dcgram_parameters[K-1], plot_label[idx], label = 'DCGram, D de 4 a 9, K={}'.format(K), linewidth = 1.0, alpha = 0.65)
        idx += 1
    # plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 1)
    plt.show()

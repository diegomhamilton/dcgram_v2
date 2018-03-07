import yaml
import matplotlib.pyplot as plt

def save_plot(parameter = 'cond_entropies', name = 'ternary_even_shift',\
                drange = range(4,10), krange = range(2,8)):
    dcgram_parameters = [[None] * len(drange) for i in range(krange[-1])]
    dcgram_states = [[None] * len(drange) for i in range(krange[-1])]
    dmark_parameters = [None] * len(drange)
    dmark_states = [None] * len(drange)

    for D in drange:
        with open('../dcgram_files/{}/results/{}/dmarkov/dmark_D{}.yaml'.format(name, parameter, D), 'r') as f:
            dmark_parameters.append(yaml.load(f))
        with open('../dcgram_files/{}/results/machines/dmarkov/dmark_D{}.yaml'.format(name, D), 'r') as f:
            machine = yaml.load(f)
            dmark_states.append(len(machine.states))

        for K in krange:
            with open('../dcgram_files/{}/results/{}/dcgram/dcgram_D{}_K{}.yaml'.format(name, parameter, D, K), 'r') as f:
                dcgram_parameters[K-1].append(yaml.load(f))
            with open('../dcgram_files/{}/results/machines/dcgram/dcgram_D{}_K{}.yaml'.format(name, D, K), 'r') as f:
                machine = yaml.load(f)
                dcgram_states[K-1].append(len(machine.states))
    plt.plot(dmark_states, dmark_parameters, 'g^-')
    plt.xscale('log')
    idx = 0
    plot_label = ['b^-', 'c^-', 'm^-', 'y^-', 'k^-', 'r^-']
    for K in krange:
        plt.plot(dcgram_states[K-1], dcgram_parameters[K-1], plot_label[idx])
        idx += 1
    plt.show()

import sys
sys.path.insert(0, '../')

import yaml
import numpy as np
import sequenceanalyzer as sa
import matplotlib.pyplot as plt
import eigenvectorcalcs as eig
from scipy.stats import kstest, ks_2samp

# rs = [3.75, 3.7499999, 3.749999, 3.74999, 3.7499, 3.749, 3.748, 3.747, 3.6, 3.65, 3.7, 3.8]
rs = [3.7499999, 3.749999, 3.74999, 3.7499, 3.749, 3.745]

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

def calc_mean_vector(machine, sequence, N):
    average = []
    for i in range(1000):
        average.append(sa.calc_occup_vector(machine, sequence[i*N:], N))
    mean = np.mean(average, axis = 0)
    d = []
    # for i in range(len(average[0])):
    #     d.append([abs(a[i] - calc_occup[i]) for a in average])

    for v in average:
        d.append(np.linalg.norm(calc_occup - v))
    print(f'erro medio = {np.mean(d)}')  
    return mean, np.std(average, axis = 0), average

def plot_bar(vec1, std1, vec2, std2, r = 3.75, x0 = 0.5):
    pos = list(range(len(vec1))) 
    width = 0.25
    fig, ax = plt.subplots(figsize=(10,5))

    plt.bar([p + width for p in pos],
            vec1,
            width,
            alpha = 1.0,
            color = '#000000',
            label = 'A')

    plt.bar([p + 2*width for p in pos],
            vec2,
            width,
            alpha = 1.0,
            color = '#808080',
            label = 'B')
    
    plt.errorbar([p + width for p in pos],
            vec1,
            yerr = std1,
            color = 'r',
            fmt = 'none',
            label = 'Er2')
    plt.errorbar([p + 2*width for p in pos],
            vec2,
            yerr = std2,
            color = 'r',
            fmt = 'none',
            label = 'Er1')
    ax.set_ylabel('Probabilidade de ocupação')
    ax.set_xticks([p + 1.5 * width for p in pos])
    ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim([0, 0.3])
    plt.legend(['$x_0 = 0.5$, $r = 3.75$', f'$x_0={x0}$, $r={r}$'], loc='upper left')
    plt.show()

def plot_box(vec1, vec2, r = 3.75, x0 = 0.5):
    pos = list(range(len(vec1[0]))) 
    width = 0.25
    fig, ax = plt.subplots(figsize=(10,5))
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    vec1 = vec1.T
    vec2 = vec2.T
    # print(vec1[0])
    print(len(vec1))
    print(len(pos))
    for i in range(len(pos)):
        b1 = plt.boxplot(vec1[i],
                positions = [pos[i] + width],
                notch=False,
                widths = width,
                sym = '.',
                patch_artist = True,
                boxprops=dict(facecolor="blue", color="blue", alpha=0.7),
                medianprops=dict(color="black"))
        b2 = plt.boxplot(vec2[i],
                positions = [pos[i] + 2*width],
                notch=False,
                widths = width,
                sym = '.',
                patch_artist = True,
                boxprops=dict(facecolor="red", color="red", alpha=0.7),
                medianprops=dict(color="black"))
        ax.vlines(x=[(p + 0.38) for p in pos], ymin=0.0, ymax=1.0, colors = 'k', linestyles = 'dashed', zorder=1)


    
    ax.set_ylabel('Probabilidade de ocupação')
    ax.set_xlabel('Nomenclatura dos estados')
    ax.set_xticks([p + 1.5 * width for p in pos])
    ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim([0, 0.25])
    plt.legend(['$x_0 = 0.5$, $r = 3.75$', f'$x_0={x0}$, $r={r}$'], loc='upper right')
    plt.show()

if __name__ == "__main__":
    with open('../../dcgram_files/logistic_map/results/machines/dcgram/dcgram_D4_n1_K5.yaml', 'r') as f:
        m = yaml.load(f)
    with open('../../dcgram_files/logistic_map/original/original_len_10000000.yaml', 'r') as f:
        s = yaml.load(f)
    calc_occup = eig.occup_vector(m)
    stable, stable_std, stable_full = calc_mean_vector(m, s, 10000)
    print(f'Standard Deviation for original system: {np.linalg.norm(stable_std)}')
    f = lambda x: (3.75-x)/3.75
    for r in rs:
        lm_s = logistic_map(0.5, r)
        lm, lm_std, lm_full = calc_mean_vector(m, lm_s, 10000)
        mean_s = []
        mean_p = []
        for i in range(len(lm_full[0])):
            stat, p_val = ks_2samp([v[i] for v in lm_full], [v[i] for v in stable_full])
            mean_s.append(stat)
            mean_p.append(p_val)
        mean_s = np.mean(np.array(mean_s))
        mean_p = np.mean(np.array(mean_p))
        percent = f(r)
        print(f'Avg Kolmogorov-Smirnov (percent = {percent}): stat = {mean_s}, p = {mean_p}')
        print('end')

        #print(f'Standard Deviation for Logistic Map with r = {r}: {np.linalg.norm(lm_std)}')
        #d = np.linalg.norm(stable - lm)
        #print(f'Distance between original system and for Logistic Map with r = {r}: {d}')
        print() 
        # plot_bar(stable, stable_std, lm, lm_std, r = r, x0 = 0.5)
        #plot_box(stable_full, lm_full, r=r, x0=0.5)

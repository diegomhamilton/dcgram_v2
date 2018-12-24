import dcgram

label_size = 1
# D = 2
name = 'duffing_equation'
krange = [3, 5, 7]
L = 1250000

for D in [2]:
    dcgram.DCGraM(name=name, D=D, krange=krange, load_original_sequence=False, load_machines=True, calc_metrics=True, L = L)
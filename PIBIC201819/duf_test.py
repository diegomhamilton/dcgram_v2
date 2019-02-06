import duffing_equation as duf

betas = [(0.1, 'beta010'), (0.12, 'beta012'), (0.14, 'beta014'), (0.16, 'beta016'), (0.18, 'beta018'), (0.2, 'beta020'), (0.22, 'beta022')]

for beta, v in betas:
    duf.generate_time_series(beta = beta, version = v)
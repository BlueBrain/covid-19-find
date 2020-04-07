from .simulation.covidlib import simulate
from io import StringIO
import pandas as pd
import numpy as np
import os.path


class Simulator:

    def run(self):
        path_prefix = os.path.abspath(os.path.dirname(__file__))
        simsfile = os.path.join(path_prefix, 'simulation', 'compart_params.csv')
        betafile = os.path.join(path_prefix, 'simulation', 'betas.csv')
        sims = pd.read_csv(simsfile, header=None)
        (rows, cols) = sims.shape
        p = {}
        for i in range(0, rows):
            p[sims.iloc[i, 0]] = []
            for j in range(1, cols):
                p[sims.iloc[i, 0]].append(sims.iloc[i, j])

        num_compartments = cols - 1

        beta_table = pd.read_csv(betafile, header=None)
        (rows, cols) = beta_table.shape
        beta = np.zeros((num_compartments, num_compartments))
        for i in range(1, num_compartments + 1):
            for j in range(1, num_compartments + 1):
                beta[i - 1, j - 1] = beta_table.iloc[i, j]

        df = simulate(num_compartments, p, beta)
        buffer = StringIO()

        buffer.seek(0)
        return df.to_csv()

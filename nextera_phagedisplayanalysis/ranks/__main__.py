import sys
from nextera_phagedisplayanalysis.ranks.ranks_plotter import RanksPlotter
from nextera_utils.docker_interop import DockerInterop
import pandas as pd
import numpy as np


print('Creating Ranks report...')

# fn = 'C:/docker_data_exchange/in/3078a211-b398-43e9-9137-0e5d983d64f9/arguments.csv'
# docker = DockerInterop(fn, '3078a211-b398-43e9-9137-0e5d983d64f9');
docker = DockerInterop(sys.argv[1])

data_items = docker.get_data_items()
for item in data_items:
    data_df = docker.read_csv(item[0], 0, na_values=[''])
    ranks_plotter = RanksPlotter(data_df)
    ranks_plotter.plot(item[1])



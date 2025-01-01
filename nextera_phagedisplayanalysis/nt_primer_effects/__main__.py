import sys
from nextera_phagedisplayanalysis.nt_primer_effects.primer_effects_plotter import PrimerEffectsPlotter
from nextera_utils.docker_interop import DockerInterop

print('Creating Nt Primer Effects report...')

# fn = "C:/docker_data_exchange/in/a7207e93-7121-42cc-9542-9f25d66e5485/arguments.csv"
# docker = DockerInterop(fn, 'a7207e93-7121-42cc-9542-9f25d66e5485');
docker = DockerInterop(sys.argv[1])

data_items = docker.get_data_items()
for item in data_items:
    data_df = docker.read_csv(item[0])
    plotter = PrimerEffectsPlotter(data_df)
    plotter.plot(item[1])
    pass
import sys

from nextera_phagedisplayanalysis.diversity.diversity_plotter import DiversityPlotter
from nextera_utils.docker_interop import DockerInterop

print('Creating Diversity report...')

# fn = "C:/docker_data_exchange/in/462447df-6e01-47c3-8b85-c615b6dfdc55/arguments.csv"
# docker = DockerInterop(fn, '462447df-6e01-47c3-8b85-c615b6dfdc55');
docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
for fn in zip(input_fns, output_fns):
    data_df = docker.read_csv(fn[0], 0)
    diversity_plotter = DiversityPlotter(data_df)
    diversity_plotter.plot(fn[1])



import sys

from nextera_phagedisplayanalysis.diversity.diversity_plotter import DiversityPlotter
from nextera_utils.docker_interop import DockerInterop

print('Creating Diversity report...')

# fn = "C:/temp/py_ncm/a7119b1e-9541-4a32-b9f2-4395a27caa43/arguments.csv"
# docker = DockerInterop(fn, 'a7119b1e-9541-4a32-b9f2-4395a27caa43');
docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
for fn in zip(input_fns, output_fns):
    data_df = docker.read_csv(fn[0], 0)
    diversity_plotter = DiversityPlotter(data_df)
    diversity_plotter.plot(fn[1])



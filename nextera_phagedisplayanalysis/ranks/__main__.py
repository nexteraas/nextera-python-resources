import sys

from nextera_phagedisplayanalysis.ranks.ranks_plotter import RanksPlotter
from nextera_utils.docker_interop import DockerInterop

print('Creating Ranks report...')
# for a in sys.argv:
#     print('arg: ' + a)

# fn = 'C:/docker_data_exchange/in/a7119b1e-9541-4a32-b9f2-4395a27caa43/arguments.csv'
# docker = DockerInterop(fn, 'a7119b1e-9541-4a32-b9f2-4395a27caa43');

docker = DockerInterop(sys.argv[1])


print(docker.get_input_filenames()[1])
input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
for fn in zip(input_fns, output_fns):
    data_df = docker.read_csv(fn[0], 0)
    ranks_plotter = RanksPlotter(data_df)
    ranks_plotter.plot(fn[1])



import sys

from nextera_phagedisplayanalysis.sampling_probabilities.sampling_probabilities_plotter import SamplingProbabilitiesPlotter
from nextera_utils.docker_interop import DockerInterop

print('Creating sampling probabilities report...')
# for a in sys.argv:
#     print('arg: ' + a)


#fn = 'C:/docker_data_exchange/in/81aa2a3e-c7b4-421f-bfd5-15778dff025b/arguments.csv'
#docker = DockerInterop(fn, '81aa2a3e-c7b4-421f-bfd5-15778dff025b');

docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
for fn in zip(input_fns, output_fns):
    data_df = docker.read_csv(fn[0])
    sampling_props_plotter = SamplingProbabilitiesPlotter(data_df)
    if 'Details_' in fn[0]:
        sampling_props_plotter.plot_details(fn[1])
    else:
        sampling_props_plotter.plot_overview(fn[1])



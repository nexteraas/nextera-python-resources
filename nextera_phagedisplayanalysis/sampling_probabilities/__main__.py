import sys

from nextera_phagedisplayanalysis.sampling_probabilities.sampling_probabilities_plotter import SamplingProbabilitiesPlotter
from nextera_utils.docker_interop import DockerInterop

print('Creating sampling probabilities report...')


#fn = 'C:/docker_data_exchange/in/5b08b79e-2162-46c8-a657-a3c17b0b3ad3/arguments.csv'
#docker = DockerInterop(fn, '5b08b79e-2162-46c8-a657-a3c17b0b3ad3');

docker = DockerInterop(sys.argv[1])

# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()
data_items = docker.get_data_items()
for item in data_items:
    data_df = docker.read_csv(item[0])
    sampling_props_plotter = SamplingProbabilitiesPlotter(data_df)
    if 'Details_' in item[0]:
        sampling_props_plotter.plot_details(item[1])
    else:
        sampling_props_plotter.plot_overview(item[1])



import sys
#import nextera_utils.utils as utils
import nextera_utils.heatmap_plotter as utils_heatmap_plotter
from nextera_utils.docker_interop import DockerInterop

print('Creating quality control report...')

# fn = "C:/docker_data_exchange/in/281d8877-ddef-4e89-ac12-444b9088dac0/arguments.csv"
# docker = DockerInterop(fn, '281d8877-ddef-4e89-ac12-444b9088dac0');

docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
summarize_fractions=True

for fns in zip(input_fns, output_fns):
    in_fn = fns[0]
    out_fn= fns[1]
    tag=docker.get_tag(in_fn)
    df = docker.read_csv(in_fn, 0)
    title = ''
    heatmap_plotter = utils_heatmap_plotter.HeatmapPlotter(df, title, sns_cmap='rocket')
    heatmap_plotter.plot(out_fn)
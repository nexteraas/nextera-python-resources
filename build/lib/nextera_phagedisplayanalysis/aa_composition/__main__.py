import sys
#import nextera_utils.utils as utils
from nextera_phagedisplayanalysis.aa_composition.aa_evolution_plotter import AaEvolutionPlotter
import nextera_utils.heatmap_plotter as utils_heatmap_plotter
from nextera_utils.docker_interop import DockerInterop

print('Creating aa composition report...')

# fn = "C:/docker_data_exchange/in/4bb6c977-fe50-41ca-be94-0eeda5f12f6c/arguments.csv"
# docker = DockerInterop(fn, '4bb6c977-fe50-41ca-be94-0eeda5f12f6c');

docker = DockerInterop(sys.argv[1])

data_items = docker.get_data_items()
# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()
summarize_fractions=True

for item in data_items:
    in_fn = item[0]
    out_fn = item[1]
    tag = item[3]
    if tag == "aa_composition":
        df = docker.read_csv(in_fn, 0)
        title = ''
        heatmap_plotter = utils_heatmap_plotter.HeatmapPlotter(df, title, sns_cmap='rocket')
        heatmap_plotter.plot(out_fn)
    elif tag == "aa_evolution":
        df = docker.read_csv(in_fn)
        evolution_plotter = AaEvolutionPlotter(df)
        evolution_plotter.plot(out_fn)

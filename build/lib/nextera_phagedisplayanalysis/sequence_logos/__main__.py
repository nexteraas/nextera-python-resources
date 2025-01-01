from nextera_phagedisplayanalysis.sequencing_comparison.heatmap_plotter import HeatmapPlotter
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils
import sys
from nextera_phagedisplayanalysis.sequence_logos.sequence_logo_plotter import SequenceLogoPlotter
from nextera_phagedisplayanalysis.sequence_logos.heatmap_plotter import HeatmapPlotter
import matplotlib.pyplot as plt
import seaborn as sns


print('Creating Sequence logos report...')

#fn = "C:/docker_data_exchange/in/260a4fdf-43f1-49f4-b018-d4201e780876/arguments.csv"
#docker = DockerInterop(fn, '260a4fdf-43f1-49f4-b018-d4201e780876');

docker = DockerInterop(sys.argv[1])

# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()
data_items = docker.get_data_items()
summarize_fractions = docker.get_info_value(0, 'summarize_fractions')
for item in data_items:
    in_fn = item[0]
    out_fn = item[1]
    tag = item[3]
    df = docker.read_csv(in_fn, 0)
    if tag == 'heatmap':
        sequence=None
        heatmap_plotter=HeatmapPlotter(df, '', 'Reds', summarize_fractions, sequence)
        heatmap_plotter.plot(out_fn)
    elif tag=='logo':
        logoPlotter=SequenceLogoPlotter(df, summarize_fractions);
        logoPlotter.plot(out_fn, '')



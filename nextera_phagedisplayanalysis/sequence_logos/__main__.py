from nextera_phagedisplayanalysis.sequencing_comparison.heatmap_plotter import HeatmapPlotter
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils
import sys
from nextera_phagedisplayanalysis.sequence_logos.sequence_logo_plotter import SequenceLogoPlotter
from nextera_phagedisplayanalysis.sequence_logos.heatmap_plotter import HeatmapPlotter
import matplotlib.pyplot as plt
import seaborn as sns


print('Creating Sequence logos report...')

# fn = "C:/docker_data_exchange/in/72f883f7-48f4-4c37-b04e-ef3febbea841/arguments.csv"
# docker = DockerInterop(fn, '72f883f7-48f4-4c37-b04e-ef3febbea841');

docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
summarize_fractions = docker.get_info_value(0, 'summarize_fractions')
for fns in zip(input_fns, output_fns):
    in_fn = fns[0]
    out_fn = fns[1]
    tag = docker.get_tag(in_fn)
    df = docker.read_csv(in_fn, 0)
    if tag == 'heatmap':
        sequence=None
        heatmap_plotter=HeatmapPlotter(df, '', 'Reds', summarize_fractions, sequence)
        heatmap_plotter.plot(out_fn)
    elif tag=='logo':
        logoPlotter=SequenceLogoPlotter(df, summarize_fractions);
        logoPlotter.plot(out_fn, '')



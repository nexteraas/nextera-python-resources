import sys
import nextera_utils.utils as utils
from nextera_utils.docker_interop import DockerInterop

print('Creating quality control report...')

# fn = "C:/docker_data_exchange/in/9f7445d8-f17c-4bf7-b6bd-dcf370cf95f9/arguments.csv"
#
# docker = DockerInterop(fn, '9f7445d8-f17c-4bf7-b6bd-dcf370cf95f9');

docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
summarize_fractions=True

for fns in zip(input_fns, output_fns):
    in_fn = fns[0]
    out_fn= fns[1]
    print (out_fn)
    tag=docker.get_tag(in_fn)
    if (tag == 'paired_gene_usage'):
        data_df = docker.read_csv(in_fn, 0)
        data_df = data_df.transpose()
        utils.plot_single_heatmap(data_df, summarize_fractions, out_fn)
        #heatmap_plotter = HeatmapPlotter(data_df, summarize_fractions)
        #heatmap_plotter.plot_single_heatmap(out_fn)


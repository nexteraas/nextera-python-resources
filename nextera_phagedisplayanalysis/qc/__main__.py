import sys
#import nextera_utils.utils as utils
import nextera_utils.heatmap_plotter as utils_heatmap_plotter
from nextera_utils.docker_interop import DockerInterop

print('Creating quality control report...')

# fn = "C:/docker_data_exchange/in/b64efe4e-0673-4ecc-8f5e-eeb279f7517a/arguments.csv"
# docker = DockerInterop(fn, 'b64efe4e-0673-4ecc-8f5e-eeb279f7517a');

docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
summarize_fractions=True

for fns in zip(input_fns, output_fns):
    in_fn = fns[0]
    out_fn= fns[1]
    print (out_fn)
    tag=docker.get_tag(in_fn)
    if tag == 'paired_gene_usage':
        df = docker.read_csv(in_fn, 0)
        df = df.transpose()
        if summarize_fractions:
            title = "Sum of fractions"
        else:
            title = "Counts"
        heatmap_plotter=utils_heatmap_plotter.HeatmapPlotter(df, title, sns_cmap='rocket')
        heatmap_plotter.plot(out_fn)
    elif tag == 'peptide_composition':
        df = docker.read_csv(in_fn, 0)
        title = ''
        heatmap_plotter = utils_heatmap_plotter.HeatmapPlotter(df, title, sns_cmap='rocket')
        heatmap_plotter.plot(out_fn)
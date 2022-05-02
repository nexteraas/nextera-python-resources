import sys

from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circos_executor import CircosExecutor
from nextera_phagedisplayanalysis.paired_genes_circos_plots.panning_path_plotter import PanningPathPlotter

print('Creating paired gene circos plots report...')

#fn = "C:/docker_data_exchange/in/cfe2bdf8-7014-449d-ac11-0558c9b50fce/arguments.csv"
#docker = DockerInterop(fn, 'cfe2bdf8-7014-449d-ac11-0558c9b50fce');

docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()

summarize_fractions=docker.get_info_value(0, 'summarizeFractions')
if summarize_fractions.upper()=='TRUE':
    summarize_fractions=True
else:
    summarize_fractions=False

label_size=docker.get_info_value(0, 'circosLabelSize')

for fns in zip(input_fns, output_fns):
    in_fn = fns[0]
    out_fn= fns[1]
    CircosExecutor.execute_circos(label_size, in_fn, out_fn)

counter=len(input_fns)
infos=docker.get_infos()
for key, info in infos.items():
    if key!='0':
        images = {}
        for i in range(0, len(info), 2):
            images[info[i]] = info[i+1]
        plotter = PanningPathPlotter(image_original_size=3000, image_display_size=750,
                                     images=images, label_height=25)
        out_fn = docker.get_output_filenames()[counter]
        plotter.plot(out_fn)
        counter += 1



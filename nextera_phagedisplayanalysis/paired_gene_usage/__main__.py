import sys

from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circos_executor import CircosExecutor
from nextera_phagedisplayanalysis.paired_gene_usage.panning_path_plotter import PanningPathPlotter
import nextera_utils.heatmap_plotter as utils_heatmap_plotter


print('Creating paired gene circos plots report...')

# fn = "C:/docker_data_exchange/in/e26fbdda-54a5-415f-b0ca-109701f16d75/arguments.csv"
# docker = DockerInterop(fn, 'e26fbdda-54a5-415f-b0ca-109701f16d75');

docker = DockerInterop(sys.argv[1])

data_items = docker.get_data_items()
# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()

summarize_fractions = docker.get_info_value(0, 'summarizeFractions')
if summarize_fractions.upper() == 'TRUE':
    summarize_fractions = True
else:
    summarize_fractions = False

label_size = docker.get_info_value(0, 'circosLabelSize')
circos_radius = docker.get_info_value(0, 'circosRadius')
circos_label_space = docker.get_info_value(0, 'circosLabelSpace')
circos_label_space = 'dims(image,radius)-' + str(circos_label_space) + 'p'
path_out_fns = []

for item in data_items:
    in_fn = item[0]
    out_fn= item[1]
    tag = item[3]
    if tag == 'heatmap':
        df = docker.read_csv(in_fn, 0)
        df = df.transpose()
        if summarize_fractions:
            title = "Sum of fractions"
        else:
            title = "Counts"
        heatmap_plotter = utils_heatmap_plotter.HeatmapPlotter(df, title, sns_cmap='rocket')
        heatmap_plotter.plot(out_fn)
    elif tag == "path":
        path_out_fns.append(out_fn)
    else:
        CircosExecutor.execute_circos(label_size, circos_radius, circos_label_space, in_fn, out_fn)

counter = 0
infos = docker.get_infos()
for key, info in infos.items():
    if key != '0':
        images = {}
        for i in range(0, len(info), 2):
            images[info[i]] = info[i+1]
        plotter = PanningPathPlotter(image_original_size=3000, image_display_size=750,
                                     images=images, label_height=25)
        out_fn = path_out_fns[counter]
        plotter.plot(out_fn)
        counter += 1



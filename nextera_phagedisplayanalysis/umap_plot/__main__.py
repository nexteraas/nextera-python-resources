import sys
from nextera_phagedisplayanalysis.umap_plot.umap_plotter import UmapPlotter
from nextera_utils.docker_interop import DockerInterop


print('Creating UMAP report...')

# fn = 'C:/docker_data_exchange/in/94940677-dfe0-46af-9ae5-d693b7147bc9/arguments.csv'
# docker = DockerInterop(fn, '94940677-dfe0-46af-9ae5-d693b7147bc9');

docker = DockerInterop(sys.argv[1])

# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()
data_items = docker.get_data_items()
item = data_items[0]

n_neighbors=int(docker.get_info_value(0,'n_neighbors'))
min_dist=float(docker.get_info_value(0,'min_dist'))
n_components=int(docker.get_info_value(0,'n_components'))
metric=docker.get_info_value(0,'metric')

data_df = docker.read_csv(item[0], 0)
umap_plotter = UmapPlotter(data_df, n_neighbors, min_dist, n_components, metric)
umap_plotter.plot(item[1], False, False, None)

if len(data_items)>1:
    item = data_items[1]
    data_df = docker.read_csv(item[0], 0)
    umap_plotter.plot(item[1], True, True, data_df)

# for fn in zip(input_fns, output_fns):
#     data_df = docker.read_csv(fn[0], 0)
#     umap_plotter = UmapPlotter(data_df, True, True)
#     umap_plotter.plot(fn[1], colors)



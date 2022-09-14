import sys
from nextera_phagedisplayanalysis.umap_plot.umap_plotter import UmapPlotter
from nextera_utils.docker_interop import DockerInterop


print('Creating UMAP report...')

fn = 'C:/docker_data_exchange/in/8fa55a33-9442-4e3c-84a2-a3f282a5adf5/arguments.csv'
#docker = DockerInterop(fn, '8fa55a33-9442-4e3c-84a2-a3f282a5adf5');
docker = DockerInterop(sys.argv[1])

print(docker.get_input_filenames()[0])
input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
n_neighbors=int(docker.get_info_value(0,'n_neighbors'))
min_dist=float(docker.get_info_value(0,'min_dist'))
n_components=int(docker.get_info_value(0,'n_components'))
metric=docker.get_info_value(0,'metric')

data_df = docker.read_csv(input_fns[0], 0)
umap_plotter = UmapPlotter(data_df, n_neighbors, min_dist, n_components, metric)
umap_plotter.plot(output_fns[0], False, False, None)

if len(input_fns)>1:
    data_df = docker.read_csv(input_fns[1], 0)
    umap_plotter.plot(output_fns[1], True, True, data_df)

# for fn in zip(input_fns, output_fns):
#     data_df = docker.read_csv(fn[0], 0)
#     umap_plotter = UmapPlotter(data_df, True, True)
#     umap_plotter.plot(fn[1], colors)



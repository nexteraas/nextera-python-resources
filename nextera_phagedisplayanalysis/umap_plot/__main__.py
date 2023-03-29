import sys
from nextera_phagedisplayanalysis.umap_plot.umap_plotter import UmapPlotter
from nextera_utils.docker_interop import DockerInterop


print('Creating UMAP report...')

# fn = 'C:/docker_data_exchange/in/6a619555-f226-4665-8aba-27df19c2dc4d/arguments.csv'
# docker = DockerInterop(fn, '6a619555-f226-4665-8aba-27df19c2dc4d');
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



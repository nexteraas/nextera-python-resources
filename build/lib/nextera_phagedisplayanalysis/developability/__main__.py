from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.developability import predictor_plotter, di_calculator
from nextera_phagedisplayanalysis.developability import umap_plotter as u
import pandas as pd
import sys


print('Creating Developability report...')


def create_di_report(di_estimation_mode):
    q_in_fn = None
    q_fig_out_fn = None
    q_tbl_out_fn = None
    di = None
    di_out = None
    predictor = None
    for item in data_items:
        in_fn = item[0]
        fig_out_fn = item[1]
        tbl_out_fn = item[2]
        tag = item[3]
        if tag == 'abs_value':
            data_df = docker.read_csv(in_fn)
            predictor = predictor_plotter.PredictorPlotter(data_df)
            predictor.calculate_developability()
            predictor.plot_data(tbl_out_fn)
        elif tag == 'quartile':
            q_in_fn = in_fn
            q_fig_out_fn = fig_out_fn
            q_tbl_out_fn = tbl_out_fn
        elif tag == 'dis':
            di = di_calculator.DiCalculator(scale=False, di_estimation_mode=di_estimation_mode)
            di_out = tbl_out_fn
            mse, mae = di.train()
            print('MSE:\t' + str(mse))
            data_df = docker.read_csv(in_fn)
    predictor.plot_quartiles(q_tbl_out_fn)
    predictor.plot_air_representations(q_fig_out_fn)
    if di is not None:
        di.predict(predictor.get_developability_df(), di_out)

def extract_filename(path):
    out = path.split('/')
    out = out[-1]
    out = out.replace("tbl.csv", "")
    return out

def create_umap_report(n_neighbors, min_dist, n_components, metric, legend_size, point_size, alpha):
    umap_out_fn=''
    abs_value_dfs=[]
    abs_value_names = []
    for item in data_items:
        in_fn = item[0]
        fig_out_fn = item[1]
        tbl_out_fn = item[2]
        tag = item[3]
        if tag == 'abs_value':
            data_df = docker.read_csv(in_fn)
            predictor = predictor_plotter.PredictorPlotter(data_df)
            df=predictor.calculate_developability()
            abs_value_dfs.append(df)
            abs_value_names.append(extract_filename(in_fn))
        elif tag=='UMAP':
            umap_out_fn = item[1]
    for i in range(len(abs_value_dfs)):
        df=abs_value_dfs[i]
        n=abs_value_names[i]
        df['groups'] = str(n)
    features = pd.concat(abs_value_dfs, ignore_index=True)
    data_df = features.drop('Name', axis=1)
    umap_plotter = u.UmapPlotter(df=data_df, groups_col='groups', n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components,
                                 metric=metric, legend_size=legend_size, point_size=point_size, alpha=alpha)

    umap_plotter.plot(umap_out_fn)


# fn = "C:/docker_data_exchange/in/cd513a1f-fa99-4c64-b82a-7ffaf398583c/arguments.csv"
# docker = DockerInterop(fn, 'cd513a1f-fa99-4c64-b82a-7ffaf398583c')

docker = DockerInterop(sys.argv[1])

data_items = docker.get_data_items()
analysis_mode = docker.get_info_value(0, 'analysis_mode')

if analysis_mode=='calculateDI':
    di_estimation_mode = docker.get_info_value(0, 'di_estimation_mode')
    create_di_report(di_estimation_mode)
elif analysis_mode == 'plotUMAP':
    n_neighbors = int(docker.get_info_value(0, 'n_neighbors'))
    min_dist = float(docker.get_info_value(0, 'min_dist'))
    n_components = int(docker.get_info_value(0, 'n_components'))
    metric = docker.get_info_value(0, 'metric')
    legend_size = int(docker.get_info_value(0, 'legend_size'))
    point_size = int(docker.get_info_value(0, 'point_size'))
    alpha = float(docker.get_info_value(0, 'alpha'))
    create_umap_report(n_neighbors, min_dist, n_components, metric, legend_size, point_size, alpha)



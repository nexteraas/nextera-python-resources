from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.developability import predictor_plotter, di_calculator
from nextera_phagedisplayanalysis.developability import umap_plotter as u
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


def create_umap_report():
    umap_out_fn=''
    abs_value_dfs=[]
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
        elif tag=='UMAP':
            umap_out_fn = item[1]
    features=None
    group=0
    for df in abs_value_dfs:
        df['groups'] = str(group)
        if features is None:
            features=df
        else:
            features = features.append(df, ignore_index=True)
        group += 1
    group_df = features.groups
    data_df=df = features.drop('column_name', axis=1)
    umap_plotter = u.UmapPlotter(data_df, group_df)
    umap_plotter.plot(umap_out_fn)


# fn = "C:/docker_data_exchange/in/c71cec5a-6aa0-4b60-8935-fc30adf0ff6f/arguments.csv"
# docker = DockerInterop(fn, 'c71cec5a-6aa0-4b60-8935-fc30adf0ff6f')
docker = DockerInterop(sys.argv[1])


data_items = docker.get_data_items()
di_estimation_mode = docker.get_info_value(0, 'di_estimation_mode')
analysis_mode = docker.get_info_value(0, 'analysis_mode')

if analysis_mode=='calculateDI':
    create_di_report(di_estimation_mode)
elif analysis_mode == 'calculateDI':
    create_umap_report()



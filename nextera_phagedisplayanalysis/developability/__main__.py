from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.developability import predictor_plotter, di_calculator
import sys


print('Creating Developability report...')

# fn = "C:/docker_data_exchange/in/51600e0a-44eb-4cb1-96ee-4c379a2d1e37/arguments.csv"
# docker = DockerInterop(fn, '51600e0a-44eb-4cb1-96ee-4c379a2d1e37')
docker = DockerInterop(sys.argv[1])


data_items = docker.get_data_items()
di_estimation_mode = docker.get_info_value(0, 'di_estimation_mode')

q_in_fn = None
q_fig_out_fn = None
q_tbl_out_fn = None
predictor = None
for item in data_items:
    in_fn = item[0]
    fig_out_fn = item[1]
    tbl_out_fn = item[2]
    tag = item[3]
    if tag=='abs_value':
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
        mse, mae = di.train()
        data_df = docker.read_csv(in_fn)
        di.predict(data_df, tbl_out_fn)

predictor.plot_quartiles(q_tbl_out_fn)
predictor.plot_air_representations(q_fig_out_fn)



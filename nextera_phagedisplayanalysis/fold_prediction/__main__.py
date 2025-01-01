import sys
from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.fold_prediction.boltz1_predictor import Boltz1Predictor

print('Creating fold prediction report...')

#fn = 'C:/docker_data_exchange/in/1c0f0806-8809-45c8-9216-a3525b2324dd/arguments.csv'
#docker = DockerInterop(fn, '1c0f0806-8809-45c8-9216-a3525b2324dd');
docker = DockerInterop(sys.argv[1])

predictor = docker.get_info_value(0, 'predictor')

data_items = docker.get_data_items()

if(predictor=='boltz1'):
    print('Running Boltz1 prediction...')
    accelerator = docker.get_info_value(0, 'boltz_accelerator')
    devices = docker.get_info_value(0, 'boltz_devices')
    output_format = docker.get_info_value(0, 'boltz_output_format')
    num_workers = docker.get_info_value(0, 'boltz_num_workers')
    for item in data_items:
        in_fn=item[0]
        out_fn=item[2]
        print('Input: ' + in_fn)
        boltz = Boltz1Predictor(in_fn, accelerator=accelerator, devices=devices,
                                output_format=output_format, num_workers=num_workers)
        print('Output: ' + out_fn)
        boltz.predict(out_fn)
        print('Prediction done.')
elif (predictor=='igfold'):
    print('Running IgFold prediction...')
    from nextera_phagedisplayanalysis.fold_prediction.igfold_predictor import IgFoldPredictor
    igfold = IgFoldPredictor()
    for item in data_items:
        data_df = docker.read_csv(item[0])
        in_fn=item[1]
        out_fn=item[2]
        igfold.predict(data_df, out_fn)





import sys
from datetime import date

from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.fold_prediction.igfold_predictor import IgFoldPredictor

print('Creating fold prediction report...')

# fn = 'C:/docker_data_exchange/in/0267c201-e49b-49f8-ace2-0a58d7be6e1f/arguments.csv'
# docker = DockerInterop(fn, '0267c201-e49b-49f8-ace2-0a58d7be6e1f');
docker = DockerInterop(sys.argv[1])

data_items = docker.get_data_items()
igfold = IgFoldPredictor()
for item in data_items:
    data_df = docker.read_csv(item[0])
    in_fn=item[1]
    out_fn=item[2]
    igfold.predict(data_df, out_fn)





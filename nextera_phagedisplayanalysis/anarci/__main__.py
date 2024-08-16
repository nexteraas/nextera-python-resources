import sys
from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.anarci import table_builder


print('Creating ANARCI report...')

# fn = "C:/docker_data_exchange/in/f9f867d3-dcc7-4e03-9b9e-4a5aa63f847f/arguments.csv"
# docker = DockerInterop(fn, 'f9f867d3-dcc7-4e03-9b9e-4a5aa63f847f');
docker = DockerInterop(sys.argv[1])

allowed_chain = docker.get_info_value(0, 'allowed_chain')
allowed_chain = allowed_chain.split(",")
allowed_chain = [s.strip() for s in allowed_chain]
allowed_species = docker.get_info_value(1, 'allowed_species')
allowed_species = allowed_species.split(",")
allowed_species = [s.strip() for s in allowed_species]
scheme = docker.get_info_value(2, 'scheme')

data_items = docker.get_data_items()

for item in data_items:
    in_fn = item[0]
    fig_out_fn = item[1]
    tbl_out_fn = item[2]
    tag = item[3]
    data_df = docker.read_csv(in_fn)
    builder=table_builder.TableBuilder(allowed_chain, allowed_species, scheme)
    builder.build(data_df, tbl_out_fn)

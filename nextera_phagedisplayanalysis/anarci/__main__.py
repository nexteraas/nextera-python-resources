import sys
from pyasn1_modules.rfc6031 import at_pskc_friendlyName
from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.anarci import table_builder
from nextera_phagedisplayanalysis.anarci.anarci_executor import AnarciExecutor

print('Creating ANARCI report...')

RECEPTORS_TAG = 'receptors'

#fn = "C:/docker_data_exchange/in/7607dca5-a495-4858-bf4e-4567ef8b69f1/arguments.csv"
#docker = DockerInterop(fn, '7607dca5-a495-4858-bf4e-4567ef8b69f1');
docker = DockerInterop(sys.argv[1])

allowed_chain = docker.get_info_value(0, 'allowed_chain')
allowed_chain = allowed_chain.split(",")
allowed_chain = [s.strip() for s in allowed_chain]
allowed_species = docker.get_info_value(1, 'allowed_species')
allowed_species = allowed_species.split(",")
allowed_species = [s.strip() for s in allowed_species]
scheme = docker.get_info_value(2, 'scheme')

data_items = docker.get_data_items()

def get_main_data_item():
    for item in data_items:
        tag = item[3]
        if tag==RECEPTORS_TAG:
            return item

main_item = get_main_data_item()
print('Receptor item found...')
main_df = docker.read_csv(main_item[0])
anarci = AnarciExecutor(main_df, scheme=scheme, allow=allowed_chain, allowed_species=allowed_species)
print('ANARCI running...')
main_out = anarci.run()
print('ANARCI run finished')

debug_key=DockerInterop.get_instance().get_debug_key()
if debug_key is None:
    tbl_out_fn = main_item[2]
    if tbl_out_fn is not None:
        print('Saving main output...')
        main_out.to_csv(tbl_out_fn, index=False, sep='\t')
else:
    print(main_out)

idx=0
for item in data_items:
    in_fn = item[0]
    fig_out_fn = item[1]
    tbl_out_fn = item[2]
    tag = item[3]
    #if tag=='details':
    if tag!=RECEPTORS_TAG:
        print('processing details...')
        builder = table_builder.TableBuilder(allowed_chain, allowed_species, scheme)
        print(anarci.get_numbered1()[idx])
        tmp=builder.build(anarci.get_numbered1()[idx], anarci.get_numbered2()[idx], tbl_out_fn)
        idx += 1
        print('Details processed')
        print(tmp)
    # data_df = docker.read_csv(in_fn)
    # builder=table_builder.TableBuilder(allowed_chain, allowed_species, scheme)
    # builder.build(data_df, tbl_out_fn)



#input: 1 tbl for ids, chain1 and chain2 sequences. Tag='main'
#       1 dummy tbl pr id (this is where the numbering goes) Tag='details'
#   step 1: iterate input tbls to find 'main'
#       run anarci_executor
#       this creates the 'main' tbl
#       the numbered data is also preserved
#   step 2:
#        iterate through numbered1 and numbered2 to create the details tbls

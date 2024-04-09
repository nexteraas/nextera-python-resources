import sys

from nextera_phagedisplayanalysis.diversity.diversity_plotter import DiversityPlotter
from nextera_phagedisplayanalysis.diversity.diversity_3d_plotter import Diversity3dPlotter
from nextera_utils.docker_interop import DockerInterop

print('Creating Diversity report...')

# fn = "C:/docker_data_exchange/in/857b8d88-1870-428d-a428-60118cea86b2/arguments.csv"
# docker = DockerInterop(fn, '857b8d88-1870-428d-a428-60118cea86b2');
docker = DockerInterop(sys.argv[1])

def get_ens_value(docker, name):
    out = docker.get_info_value(0, name)
    if out is not None:
        out = int(out)
    return out

data_items = docker.get_data_items()
# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()

cdr3_ens_scale_value = get_ens_value(docker, 'cdr3EnsScaleValue')
v_gene_ens_scale_value = get_ens_value(docker, 'vGeneEnsScaleValue')
peptide_ens_scale_value = get_ens_value(docker, 'peptideEnsScaleValue')
for item in data_items:
    data_df = docker.read_csv(item[0], 0)
    tag=item[3]
    if tag=='IR':
        diversity_plotter = DiversityPlotter(data_df)
        diversity_plotter.plot_ir(item[1])
    elif tag=='Peptide':
        diversity_plotter = DiversityPlotter(data_df)
        diversity_plotter.plot_peptide(item[1])
    elif tag == 'GlobalCdr3':
        diversity_plotter = Diversity3dPlotter(data_df, cdr3_ens_scale_value)
        diversity_plotter.plot(item[1])
    elif tag == 'GlobalVgene':
        diversity_plotter = Diversity3dPlotter(data_df, v_gene_ens_scale_value)
        diversity_plotter.plot(item[1])
    elif tag == 'GlobalPeptide':
        diversity_plotter = Diversity3dPlotter(data_df, peptide_ens_scale_value)
        diversity_plotter.plot(item[1])

# for fn in zip(input_fns, output_fns):
#     data_df = docker.read_csv(fn[0], 0)
#     tag=docker.get_tag(fn[0])
#     if tag=='IR':
#         diversity_plotter = DiversityPlotter(data_df)
#         diversity_plotter.plot_ir(fn[1])
#     elif tag=='Peptide':
#         diversity_plotter = DiversityPlotter(data_df)
#         diversity_plotter.plot_peptide(fn[1])
#     elif tag == 'GlobalCdr3':
#         diversity_plotter = Diversity3dPlotter(data_df, cdr3_ens_scale_value)
#         diversity_plotter.plot(fn[1])
#     elif tag == 'GlobalVgene':
#         diversity_plotter = Diversity3dPlotter(data_df, v_gene_ens_scale_value)
#         diversity_plotter.plot(fn[1])
#     elif tag == 'GlobalPeptide':
#         diversity_plotter = Diversity3dPlotter(data_df, peptide_ens_scale_value)
#         diversity_plotter.plot(fn[1])

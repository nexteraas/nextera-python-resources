from setuptools import setup

setup(
    name='nextera-python-resources',
    version='1.0.0',
    packages=['deep_sp', 'nextera_utils',
              'nextera_phagedisplayanalysis',
              'nextera_phagedisplayanalysis.anarci',
              'nextera_phagedisplayanalysis.ranks',
              'nextera_phagedisplayanalysis.developability',
              'nextera_phagedisplayanalysis.diversity',
              'nextera_phagedisplayanalysis.sequencing_comparison',
              'nextera_phagedisplayanalysis.paired_gene_usage',
              'nextera_phagedisplayanalysis.umap_plot',
              'nextera_phagedisplayanalysis.sampling_probabilities',
              'nextera_phagedisplayanalysis.qc',
              'nextera_phagedisplayanalysis.sequence_logos',
              'nextera_phagedisplayanalysis.phylogenetics',
              'nextera_phagedisplayanalysis.aa_composition',
              'nextera_phagedisplayanalysis.fold_prediction'],
    include_package_data = True,
    url='',
    license='',
    author='Ralf Neumann',
    author_email='',
    description=''
)

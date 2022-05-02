import sys
from nextera_phagedisplayanalysis.sequencing_comparison.histogram_plotter import HistogramPlotter, Mode
from nextera_phagedisplayanalysis.sequencing_comparison.histogram_plotter import Mode as histMode
from nextera_phagedisplayanalysis.sequencing_comparison.heatmap_plotter import HeatmapPlotter
from nextera_phagedisplayanalysis.sequencing_comparison.barchart_plotter import BarchartPlotter
from nextera_phagedisplayanalysis.sequencing_comparison.barchart_plotter import Mode as barMode
from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circos_executor import CircosExecutor

print('Creating Sequencing comparison report...')

# fn = "C:/docker_data_exchange/in/4b71fe78-4f10-4d2a-88a6-53b1ac78a58a/arguments.csv"
# docker = DockerInterop(fn, '4b71fe78-4f10-4d2a-88a6-53b1ac78a58a');

docker = DockerInterop(sys.argv[1])

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
summarize_fractions=docker.get_info_value(0, 'summarizeFractions')
if summarize_fractions.upper()=='TRUE':
    summarize_fractions=True
else:
    summarize_fractions=False

for fns in zip(input_fns, output_fns):
    in_fn = fns[0]
    out_fn= fns[1]
    print (out_fn)
    tag=docker.get_tag(in_fn)
    if (tag == 'paired_gene_usage') or (tag == 'complete_cdr3_length') or (tag == 'complete_gene_usage'):
        data_df = docker.read_csv(in_fn)
    else:
        data_df = docker.read_csv(in_fn, 0)
    if tag=='cdr3_usage':
        hist_plotter = HistogramPlotter(data_df, summarize_fractions, histMode.Cdr3Usage)
        hist_plotter.plot(out_fn)
    elif tag=='gene_usage':
        hist_plotter = HistogramPlotter(data_df, summarize_fractions, histMode.GeneUsage)
        hist_plotter.plot(out_fn)
    elif tag=='single_heatmap':
        heatmap_plotter = HeatmapPlotter(data_df, summarize_fractions)
        heatmap_plotter.plot_single_heatmap(out_fn)
    elif tag == 'difference_heatmaps':
        heatmap_plotter = HeatmapPlotter(data_df, summarize_fractions)
        heatmap_plotter.plot_difference_heatmaps(out_fn)
    elif tag == 'complete_cdr3_length':
        barchart_plotter = BarchartPlotter(data_df, summarize_fractions, barMode.cdr3_length)
        barchart_plotter.plot(out_fn)
    elif tag == 'complete_gene_usage':
        barchart_plotter = BarchartPlotter(data_df, summarize_fractions, barMode.gene_usage)
        barchart_plotter.plot(out_fn)


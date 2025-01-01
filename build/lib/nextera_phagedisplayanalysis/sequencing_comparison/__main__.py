import sys
from nextera_phagedisplayanalysis.sequencing_comparison.histogram_plotter import HistogramPlotter, Mode
from nextera_phagedisplayanalysis.sequencing_comparison.histogram_plotter import Mode as histMode
from nextera_phagedisplayanalysis.sequencing_comparison.heatmap_plotter import HeatmapPlotter
from nextera_phagedisplayanalysis.sequencing_comparison.barchart_plotter import BarchartPlotter
from nextera_phagedisplayanalysis.sequencing_comparison.barchart_plotter import Mode as barMode
from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circos_executor import CircosExecutor

print('Creating Sequencing comparison report...')

# fn = "C:/docker_data_exchange/in/ce6bb27c-3b5d-49fd-8546-2f3b9a0585be/arguments.csv"
# docker = DockerInterop(fn, 'ce6bb27c-3b5d-49fd-8546-2f3b9a0585be');

docker = DockerInterop(sys.argv[1])

# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()
data_items = docker.get_data_items()
summarize_fractions=docker.get_info_value(0, 'summarizeFractions')
if summarize_fractions.upper()=='TRUE':
    summarize_fractions=True
else:
    summarize_fractions=False

for item in data_items:
    in_fn = item[0]
    out_fn= item[1]
    tag = item[3]
    if (tag == 'paired_gene_usage') or (tag == 'complete_cdr3_length') or (tag == 'complete_gene_usage'):
        data_df = docker.read_csv(in_fn)
    else:
        data_df = docker.read_csv(in_fn, 0)
    if tag=='cdr3_usage':
        hist_plotter = HistogramPlotter(data_df, summarize_fractions, histMode.Cdr3Usage)
        hist_plotter.plot(out_fn)
    elif tag == 'n_inserts':
        barchart_plotter = BarchartPlotter(data_df, False, barMode.n_inserts)
        barchart_plotter.plot_n_inserts(out_fn)
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


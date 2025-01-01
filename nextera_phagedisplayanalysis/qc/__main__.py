import sys
#import nextera_utils.utils as utils
import nextera_utils.heatmap_plotter as utils_heatmap_plotter
from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circos_executor import CircosExecutor
from nextera_phagedisplayanalysis.qc.sequence_overlap_plotter import SequenceOverlapPlotter
from nextera_phagedisplayanalysis.qc.readcount_distribution_plotter import ReadcountDistributionPlotter


print('Creating quality control report...')
# fn = "C:/docker_data_exchange/in/cd41c834-0722-4878-aa4e-5e1fe65bbe63/arguments.csv"
# docker = DockerInterop(fn, 'cd41c834-0722-4878-aa4e-5e1fe65bbe63');

docker = DockerInterop(sys.argv[1])

data_items = docker.get_data_items()
# input_fns = docker.get_input_filenames()
# output_fns = docker.get_fig_output_filenames()

seq_overlap_curves = docker.get_info_value(0, 'seqOverlapCurves')
seq_overlap_curves = docker.parse_java_boolean(seq_overlap_curves)
seq_overlap_crossing_intersections = docker.get_info_value(0, 'seqOverlapCrossingIntersections')
seq_overlap_crossing_intersections = docker.parse_java_boolean(seq_overlap_crossing_intersections)
seq_overlap_curves_offCenter = docker.get_info_value(0, 'seqOverlapCurvesOffCenter')

counter=0
for item in data_items:
    in_fn = item[0]
    out_fn= item[1]
    tag=item[3]
    if tag=='peptide_composition':
        df = docker.read_csv(in_fn, 0)
        title = ''
        heatmap_plotter = utils_heatmap_plotter.HeatmapPlotter(df, title, sns_cmap='rocket')
        heatmap_plotter.plot(out_fn)
    elif tag=='seq_overlap':
        df = docker.read_csv(in_fn, None)
        seq_overlap_plotter=SequenceOverlapPlotter(df, seq_overlap_curves, seq_overlap_crossing_intersections)
        seq_overlap_plotter.plot(out_fn)
    elif tag == 'rc_distribution':
        df = docker.read_csv(in_fn, None)
        rc_dist_plotter = ReadcountDistributionPlotter(df)
        rc_dist_plotter.plot(out_fn)

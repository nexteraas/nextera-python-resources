from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.phylogenetics.phylo_plotter import PhyloPlotter
import sys


print('Creating phylogenetics report...')

# fn = "C:/docker_data_exchange/in/d1cd98df-8013-49c7-bc49-13cca7932ac6/arguments.csv"
# docker = DockerInterop(fn, 'd1cd98df-8013-49c7-bc49-13cca7932ac6');

docker = DockerInterop(sys.argv[1])

def extract_colors(docker):
    out={}
    i = 1
    while(True):
        info = docker.get_info(i)
        i += 1
        if info is None:
            break
        else:
            tmp = info[0].split('=')
            out[tmp[0]]=tmp[1]
    return out

input_fns = docker.get_input_filenames()
output_fns = docker.get_output_filenames()
tree_construction = docker.get_info_value(0, 'tree_construction')

distance_construction_method = docker.get_info_value(0, 'distance_construction_method')
default_color = docker.get_info_value(0, 'default_color')
default_size = int(docker.get_info_value(0, 'default_size'))
arc_start = int(docker.get_info_value(0, 'arc_start'))
arc_span = int(docker.get_info_value(0, 'arc_span'))
tree_style_mode = docker.get_info_value(0, 'tree_style_mode')
colors=extract_colors(docker)
plotter = PhyloPlotter(tree_construction, distance_construction_method, default_color, default_size,
                       tree_style_mode, arc_start, arc_span)
for fns in zip(input_fns, output_fns):
    in_fn = fns[0]
    out_fn = fns[1]
    tag = docker.get_tag(in_fn)
    plotter.plot(in_fn, out_fn, tag, colors)


#
#
#
# from Bio.Phylo.TreeConstruction import DistanceCalculator
# from Bio import AlignIO
# from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
#
#
#
# from ete3 import Tree as EteTree
# import tempfile
#
# def to_ete3(bioTree):
#     with tempfile.NamedTemporaryFile(mode="w") as tmp:
#         Bio.Phylo.write(bioTree.root, tmp, 'newick')
#         tmp.flush()
#         return EteTree(tmp.name)
#
#
#
# aln = AlignIO.read('C:/temp/test.fa', 'fasta')
# print(aln)
# calculator = DistanceCalculator('identity')
# dm = calculator.get_distance(aln)
# print(dm)
#
#
#
# constructor = DistanceTreeConstructor(calculator, 'nj')
# tree = constructor.build_tree(aln)
# print(tree)
#
# import Bio.Phylo
# tree.ladderize()  # Flip branches so deeper clades are displayed at top
#
# #etet=to_ete3(tree)
#
# from io import StringIO
# from ete3 import TreeStyle
#
#
# sio=StringIO()
# tree_string=""
# Bio.Phylo.write(tree,sio, "newick")
# etet=EteTree(sio.getvalue(), format=1)
# ts = TreeStyle()
# ts.show_leaf_name = True
# ts.show_branch_length = True
# ts.show_branch_support = True
#
# ts = TreeStyle()
# ts.show_leaf_name = True
# ts.mode = "c"
# ts.arc_start = -180 # 0 degrees = 3 o'clock
# ts.arc_span = 180
# etet.show(tree_style=ts)
# #etet.render("C:/temp/mytree.png", w=183, units="mm", tree_style=ts)
# exit(1)
#
# for xxx in tree.get_nonterminals():
#     print(xxx)
#     xxx.name=""
#
#
# for clade in tree.get_terminals():
#     if clade.name in "seq1":
#         clade.color = 'red'
#     else:
#         clade.color = 'blue'
# Bio.Phylo.draw(tree, axhspan=((0.25, 7.75), {'facecolor':'0.9'}), do_show=True)
#
#
#
# #import matplotlib.pyplot as plt
# #plt.savefig("TreeToCutOff.svg", format='svg', dpi=1200)
#
#

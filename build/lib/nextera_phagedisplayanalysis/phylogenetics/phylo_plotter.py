import nextera_utils.utils as utils
from nextera_utils.docker_interop import DockerInterop
import matplotlib.pyplot as plt
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, ParsimonyScorer, NNITreeSearcher, ParsimonyTreeConstructor
import Bio.Phylo
from io import StringIO
from ete3 import TreeStyle, NodeStyle
from ete3 import Tree as EteTree
import tempfile
from Bio import AlignIO



class PhyloPlotter:

    def __init__(self, tree_construction='distance', distance_construction_method='nj',
                 default_color='black', default_size=2, tree_style_mode='r',
                 arc_start=-180, arc_span=180):
        try:
            docker_interop = DockerInterop.get_instance()
            self._debug_key = docker_interop.get_debug_key()
        except:
            self._debug_key = ''
        self._tree_construction=tree_construction
        self._distance_construction_method = distance_construction_method
        self._default_color = default_color
        self._default_size = default_size
        self._arc_start = arc_start
        self._arc_span = arc_span
        self._tree_style = self._create_tree_style(tree_style_mode)

    def _create_tree_style(self, tree_style_mode):
        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.show_branch_length = True
        ts.show_branch_support = True
        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.mode = tree_style_mode
        ts.arc_start = self._arc_start
        ts.arc_span = self._arc_span
        return ts

    def plot(self, in_fn, out_fn, title, colors={}):
        aln = self._create_alinments(in_fn)
        tree = self._create_distance_tree(aln)
        if self._tree_construction=='parsimony':
            tree = self._create_parsimony_tree(aln, tree)
        tree.ladderize()
        tree_ete = self._convert_to_ete(tree)
        self._define_node_styles(tree_ete, colors)
        debug_key = self._debug_key
        if debug_key is None:
            tree_ete.render(out_fn, tree_style=self._tree_style)
            # tree_ete.render(out_fn, w=183, units="mm", tree_style=self._tree_style)
        else:
            tree_ete.show(tree_style=self._tree_style)

    def _create_alinments(self, fasta_fn):
        aln = AlignIO.read(fasta_fn, 'fasta')
        return aln

    def _create_distance_tree(self, aln):
        calculator = DistanceCalculator('identity')
        dm = calculator.get_distance(aln)
        #print(dm)
        constructor = DistanceTreeConstructor(calculator, self._distance_construction_method)
        tree = constructor.build_tree(aln)
        #print(tree)
        return tree

    def _create_parsimony_tree(self, aln, starting_tree):
        scorer = ParsimonyScorer()
        searcher = NNITreeSearcher(scorer)
        constructor = ParsimonyTreeConstructor(searcher, starting_tree)
        pars_tree = constructor.build_tree(aln)
        return pars_tree

    def _convert_to_ete(self, tree):
        sio = StringIO()
        Bio.Phylo.write(tree, sio, "newick")
        out = EteTree(sio.getvalue(), format=1)
        return out

    def _define_node_styles(self, tree, colors):
        nstyle = NodeStyle()
        nstyle["fgcolor"] = "white"
        nstyle["size"] = 0
        nstyle["hz_line_color"] = self._default_color
        nstyle["hz_line_width"] = self._default_size
        nstyle["vt_line_width"] = self._default_size
        for n in tree.traverse():
            n.set_style(nstyle)
        for seq_name, color in colors.items():
            nstyle = NodeStyle()
            nstyle["fgcolor"] = "white"
            # nstyle["shape"] = "sphere"
            nstyle["size"] = 0
            nstyle["hz_line_width"] = self._default_size
            nstyle["vt_line_width"] = self._default_size
            #nstyle["fgcolor"] = "darkred"
            nstyle["hz_line_color"] = color
            for n in tree.traverse():
                if n.name==seq_name:
                    n.set_style(nstyle)


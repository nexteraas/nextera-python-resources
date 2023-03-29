from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor



from ete3 import Tree as EteTree
import tempfile

def to_ete3(bioTree):
    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        Bio.Phylo.write(bioTree.root, tmp, 'newick')
        tmp.flush()
        return EteTree(tmp.name)



aln = AlignIO.read('C:/temp/test.fa', 'fasta')
print(aln)
calculator = DistanceCalculator('identity')
dm = calculator.get_distance(aln)
print(dm)



constructor = DistanceTreeConstructor(calculator, 'nj')
tree = constructor.build_tree(aln)
print(tree)

import Bio.Phylo
tree.ladderize()  # Flip branches so deeper clades are displayed at top

#etet=to_ete3(tree)

from io import StringIO
from ete3 import TreeStyle


sio=StringIO()
tree_string=""
Bio.Phylo.write(tree,sio, "newick")
etet=EteTree(sio.getvalue(), format=1)
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_length = True
ts.show_branch_support = True

ts = TreeStyle()
ts.show_leaf_name = True
ts.mode = "c"
ts.arc_start = -180 # 0 degrees = 3 o'clock
ts.arc_span = 180

etet.render("C:/temp/mytree.png", w=183, units="mm", tree_style=ts)

for xxx in tree.get_nonterminals():
    print(xxx)
    xxx.name=""


for clade in tree.get_terminals():
    if clade.name in "seq1":
        clade.color = 'red'
    else:
        clade.color = 'blue'
Bio.Phylo.draw(tree, axhspan=((0.25, 7.75), {'facecolor':'0.9'}), do_show=True)



#import matplotlib.pyplot as plt
#plt.savefig("TreeToCutOff.svg", format='svg', dpi=1200)



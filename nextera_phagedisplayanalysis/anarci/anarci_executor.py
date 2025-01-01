import pandas as pd
import anarci as a


class ReceptorChain(object):
    def __init__(self, id, chain, v_gene, j_gene):
        self._id=id
        self._chain=chain
        self._v_gene=v_gene
        self._j_gene=j_gene

    def get_chain(self):
        return self._chain

    def get_v_gene(self):
        return self._v_gene

    def get_j_gene(self):
        return self._j_gene

    def __str__(self):
        out=self._chain + '|' + self._v_gene + '|' + self._j_gene
        return out


class Receptor:
    def __init__(self, id, chain1, chain2):
        self._id=id
        self._chain1=chain1
        self._chain2=chain2

    def get_chain(self, index):
        if index == 1:
            return self._chain1
        elif index == 2:
            return self._chain2

    def __str__(self):
        out=self._id + '|' + str(self._chain1) + ':' + str(self._chain2)
        return out

class Chains:
    def __init__(self, alignments1, alignments2):
        self._receptors={}
        self._chain1s=self._create_receptor_chains(alignments1)
        self._chain2s=self._create_receptor_chains(alignments2)
        ids = {}
        for id, chain1 in self._chain1s.items():
            ids[id] = id
        for id, chain1 in self._chain2s.items():
            ids[id] = id
        for key, value in ids.items():
            chain1 = self._chain1s.get(key)
            chain2 = self._chain2s.get(key)
            receptor = Receptor(key, chain1, chain2)
            self._receptors[key] = receptor

    def _create_receptor_chains(self, alignments):
        out={}
        for i in range(len(alignments)):
            ali=alignments[i]
            if ali is not None:
                ali=ali[0]
                id=ali['query_name']
                chain=ali['chain_type']
                germlines=ali['germlines']
                v_gene=germlines['v_gene']
                v_gene=v_gene[0][1]
                j_gene=germlines['j_gene']
                j_gene=j_gene[0][1]
                rc=ReceptorChain(id, chain, v_gene, j_gene)
                out[id] = rc
        return out

    def get_receptors(self):
        return self._receptors

    def get_receptors_as_df(self):
        ids = []
        c1_chain = []
        c1_v_gene = []
        c1_j_gene = []
        c2_chain = []
        c2_v_gene = []
        c2_j_gene = []
        out = {}
        for id, rec in self._receptors.items():
            ids.append(id)
            c1 = rec.get_chain(1)
            c2 = rec.get_chain(2)
            if c1 is None:
                c1_chain.append('')
                c1_v_gene.append('')
                c1_j_gene.append('')
            else:
                c1_chain.append(c1.get_chain())
                c1_v_gene.append(c1.get_v_gene())
                c1_j_gene.append(c1.get_j_gene())
            if c2 is None:
                c2_chain.append('')
                c2_v_gene.append('')
                c2_j_gene.append('')
            else:
                c2_chain.append(c2.get_chain())
                c2_v_gene.append(c2.get_v_gene())
                c2_j_gene.append(c2.get_j_gene())
        out['id']=ids
        out['chain1 chain']=c1_chain
        out['chain1 V-gene'] = c1_v_gene
        out['chain1 J-gene'] = c1_j_gene
        out['chain2 chain']=c2_chain
        out['chain2 V-gene'] = c2_v_gene
        out['chain2 J-gene'] = c2_j_gene
        out_df = pd.DataFrame(out)
        return out_df


class AnarciExecutor(object):
    def __init__(self, in_df, scheme=None, allow=None, allowed_species=None):
        self._chain1, self._chain2 = self._get_anarci_input(in_df)
        self._scheme = scheme
        self._allow = allow
        self._allowed_species = allowed_species

    def _get_anarci_input(self, in_df):
        chains1=[]
        chains2=[]
        for index, row in in_df.iterrows():
            id = row['id']
            chain1 = row['chain1']
            chain2 = row['chain2']
            chains1.append((id, chain1))
            chains2.append((id, chain2))
        return chains1, chains2

    def run(self):
        if (self._scheme is None and self._allow is None and self._allowed_species is None):
            seqs1, self._numbered1, ali_details1, hit_tbls1 = a.run_anarci(self._chain1, scheme='imgt',
                                                                     assign_germline=True)
            seqs2, self._numbered2, ali_details2, hit_tbls2 = a.run_anarci(self._chain2, scheme='imgt',
                                                                     assign_germline=True)
        else:
            seqs1, self._numbered1, ali_details1, hit_tbls1 = a.run_anarci(self._chain1, scheme=self._scheme,
                                                                     allow=self._allow,
                                                                     allowed_species=self._allowed_species,
                                                                     assign_germline=True)
            seqs2, self._numbered2, ali_details2, hit_tbls2 = a.run_anarci(self._chain2, scheme=self._scheme,
                                                                     allow=self._allow,
                                                                     allowed_species=self._allowed_species,
                                                                     assign_germline=True)

        chains = Chains(ali_details1, ali_details2)
        return chains.get_receptors_as_df()

    def get_numbered1(self):
        return self._numbered1

    def get_numbered2(self):
        return self._numbered2

# col1=[]
# col2=[]
# col3=[]
#
# col1.append('12e8')
# col2.append('DIVMTQSQKFMSTSVGDRVSITCKASQNVGTAVAWYQQKPGQSPKLMIYSASNRYTGVPDRFTGSGSGTDFTLTISNMQSEDLADYFCQQYSSYPLTFGAGTKLELKRADAAPTVSIFPPSSEQLTSGGASV')
# col3.append('EVQLQQSGAEVVRSGASVKLSCTASGFNIKDYYIHWVKQRPEKGLEWIGWIDPEIGDTEYVPKFQGKATMTADTSSNTAYLQLSSLTSEDTAVYYCNAGHDYDRGRFPYWGQGTLVTVSAAKTTPPSVYPLAP')
# col1.append('5e21fd18-46b7-459e-bd9f-3ad029dbb40f')
# col2.append('DIRMTQSPSSVSASVGDRVTITCRASQGISSWLAWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQANSFPITFGQGTRLEIK')
# col3.append('QVQLQESGPGLVKPSQTLSLTCTVSGGSISSGGYYWSWIRQPAGKGLEWIGTVYHSGSTYYNPSLKSRVTISLDTSKNQFSLKLSSVTAADTAVYYCARSRDGYNYDYWGQGTLVTVSS')
#
# test_in={}
# test_in['id']=col1
# test_in['chain1']=col2
# test_in['chain2']=col3
# test_in=pd.DataFrame(test_in)
# a_exe=AnarciExecutor(test_in)
# df=a_exe.run()
# print(df)
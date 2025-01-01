from builtins import object
from deep_sp.anarci_proxy import AnarciProxy
import pandas as pd
from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.anarci import regions_annotator


class TableBuilder(object):
    def __init__(self, allowed_chain, allowed_species, scheme):
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._allowed_chain=allowed_chain
        self._allowed_species=allowed_species
        self._scheme=scheme
        self._regions_annotator=regions_annotator.RegionsAnnotator(scheme)

    # def build(self, df, out_fn):
    #     in1 = self._create_anarci_input(df, 1)
    #     in2 = self._create_anarci_input(df, 2)
    #     seq1, numbered1, ali1, hits1 = AnarciProxy.run_anarci(in1, scheme=self._scheme,
    #                                                           allow=self._allowed_chain,
    #                                                           allowed_species=self._allowed_species,
    #                                                           h_chain=False)
    #     seq2, numbered2, ali2, hits2 = AnarciProxy.run_anarci(in2, scheme=self._scheme,
    #                                                           allow=self._allowed_chain,
    #                                                           allowed_species=self._allowed_species,
    #                                                           h_chain=True)
    #     out = self._create_out_tbl(numbered1, numbered2)
    #     if self._debug_key is None:
    #         if out_fn is not None:
    #             out.to_csv(out_fn, index=False, sep='\t')
    #     else:
    #         print(out)
    #     return out

    def build(self, numbered1, numbered2, out_fn):
        cols1 = self._create_out_columns(numbered1, numbered2)
        cols2 = self._create_out_columns(numbered1, numbered2)
        print('table length:' + str(len(cols1[0])))
        self._parse_numbered(numbered1, cols1, 1)
        self._parse_numbered(numbered2, cols2, 2)
        out = self._create_out_tbl(cols1, cols2)
        if self._debug_key is None:
            if out_fn is not None:
                out.to_csv(out_fn, index=False, sep='\t')
        else:
            print(out)
        return out

    def _create_out_columns(self, numbered1, numbered2):
        col_idx=[]
        col_number=[]
        col_aa=[]
        col_region=[]
        l1 = len(numbered1[0][0])
        l2 = len(numbered2[0][0])
        l=max([l1,l2])
        for i in range(l):
            col_idx.append(0)
            col_number.append(' ')
            col_aa.append(' ')
            col_region.append(' ')
        return col_idx, col_number, col_aa, col_region

    def _parse_numbered(self, numbered, cols, chainNo):
        col_idx, col_number, col_aa, col_region = cols
        domain_numbering, start_index, end_index = numbered[0]
        count=1
        for i in range(len(cols[0])):
            col_idx[i]=count
            count+=1
            if len(domain_numbering)>i:
                pos=domain_numbering[i]
                pos_id, pos_aa=pos
                number, letter=pos_id
                col_number[i]=(str(number) + str(letter))
                col_aa[i]=pos_aa
                col_region[i]=self._regions_annotator.annotate(number, chainNo)

    def _create_out_tbl(self, cols1, cols2):
        tmp = {}
        tmp['chain1 index'] = cols1[0]
        tmp['chain1 number']=cols1[1]
        tmp['chain1 residue'] = cols1[2]
        tmp['chain1 comment'] = cols1[3]
        tmp['chain2 index'] = cols2[0]
        tmp['chain2 number'] = cols2[1]
        tmp['chain2 residue'] = cols2[2]
        tmp['chain2 comment'] = cols2[3]
        out=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in tmp.items()]))
        out = out.fillna('')
        return out

    # def _create_anarci_input(self, df, chain_no):
    #     for index, row in df.iterrows():
    #         if chain_no==1:
    #             seq = row['chain1']
    #             return seq
    #         else:
    #             seq = row['chain2']
    #             return seq

    # def _create_out_tbl(self, numbered1, numbered2):
    #     out1 = self._get_numbering(numbered1)
    #     out2 = self._get_numbering(numbered2)
    #     col1 = []
    #     col2 = []
    #     col3 = []
    #     col4 = []
    #     col5 = []
    #     col6 = []
    #     col7 = []
    #     col8 = []
    #     if out1 is None:
    #         col1.append('(No data)')
    #         col2.append('(No data)')
    #         col3.append('(No data)')
    #         col4.append('(No data)')
    #     else:
    #         count=0
    #         for item in out1:
    #             count+=1
    #             n=item[0][0]
    #             l=item[0][1]
    #             col1.append(count)
    #             col2.append(str(n) + str(l))
    #             col3.append(item[1][0])
    #             col4.append(self._regions_annotator.annotate(n, 1))
    #     if out2 is None:
    #         col5.append('(No data)')
    #         col6.append('(No data)')
    #         col7.append('(No data)')
    #         col8.append('(No data)')
    #     else:
    #         count = 0
    #         for item in out2:
    #             count += 1
    #             n = item[0][0]
    #             l = item[0][1]
    #             col5.append(count)
    #             col6.append(str(item[0][0]) + str(item[0][1]))
    #             col7.append(item[1][0])
    #             col8.append(self._regions_annotator.annotate(n, 2))
    #     tmp = {}
    #     tmp['chain1 index'] = col1
    #     tmp['chain1 number']=col2
    #     tmp['chain1 residue'] = col3
    #     tmp['chain1 comment'] = col4
    #     tmp['chain2 index'] = col5
    #     tmp['chain2 number'] = col6
    #     tmp['chain2 residue'] = col7
    #     tmp['chain2 comment'] = col8
    #     out=pd.DataFrame(dict([(k, pd.Series(v)) for k, v in tmp.items()]))
    #     out = out.fillna('')
    #     return out
    #
    # def _get_numbering(self, numbered):
    #     out=[]
    #     for seq in numbered:
    #         if seq==None:
    #             return None
    #         for region in seq:
    #             for pos in region[0]:
    #                 out.append(pos)
    #     return out

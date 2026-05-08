class AaSequenceMap(object):
    def __init__(self, fn, sequences=None, remove_gaps=False, productive_only=True, tag=None):
        self._fn = fn
        self._remove_gaps = remove_gaps
        self._productive_only = productive_only
        self._tag = tag
        if sequences is None:
            self._sequences = {}
            self._read()
        else:
            self._sequences = sequences

    def _read(self):
        with open(self._fn, 'r') as file:
            lines = file.readlines()
        this_key = None
        for line in lines:
            if line.startswith('>'):
                this_key = line[1:].strip()
                # if self._sequences.get(this_key) is not None:
                #     raise Exception(f"Duplicated header: {this_key}")
                self._sequences[this_key] = ''
            else:
                s = line.upper().strip()
                if self._remove_gaps:
                    s = s.replace('-', '')
                self._sequences[this_key] += s
        if self._productive_only:
            self._remove_unproductive()

    def get_unique_sequences(self):
        tmp={}
        out_seqs={}
        for key, seq in self._sequences.items():
            x = tmp.get(seq)
            if x is None:
                tmp[seq]=seq
                out_seqs[key] = seq
        out = AaSequenceMap(self._fn, sequences=out_seqs, remove_gaps=self._remove_gaps,
                            productive_only=self._productive_only, tag=self._tag)
        return out

    def get_tag(self):
        if self._tag is None:
            return self._fn
        else:
            return self._tag

    def _remove_unproductive(self):
        keys_to_remove = [key for key, value in self._sequences.items() if '*' in value]
        for key in keys_to_remove:
            del self._sequences[key]

    def get_sequences(self):
        return self._sequences

    def get_fn(self):
        return self._fn

    def get_remove_gaps(self):
        return self._remove_gaps

    def get_productive_only(self):
        return self._productive_only

    def get_sequence_list(self):
        out=[]
        for s in self._sequences.values():
            out.append(s)
        return out

    def get_id_list(self):
        out=[]
        for s in self._sequences.keys():
            out.append(s)
        return out

    def get_map(self):
        out = {}
        for k, v in self._sequences.items():
            out[k] = v
        return out

    def remove_sequences(self, disallowed_text=[]):
        #disallowed_aas = [aa.upper() for aa in disallowed_aas]
        keys_to_remove = []
        for key, value in self._sequences.items():
            for t in disallowed_text:
                if t in value:
                    keys_to_remove.append(key)
                    break
        #keys_to_remove = [key for key, value in self._sequences.items() if
        #                  self._contains_any_char(value, disallowed_aas)]
        for key in keys_to_remove:
            del self._sequences[key]
        return len(keys_to_remove)

    def _contains_any_char(self, target_string, char_list):
        return any(char in target_string for char in char_list)

    def write(self, fn):
        with open(fn, "w") as f:
            for k, v in self._sequences.items():
                f.write(">" + k + "\n")
                f.write(v + "\n")




class CuratingAaSequenceMap(AaSequenceMap):
    def curate_paired_sequences_by_truncation(self, first_chain_vtrim, first_chain_rtrim,
                                              second_chain_vtrim, second_chain_rtrim, sep=':'):
        new_seqs={}
        for k, v in self._sequences.items():
            new_s = self._curate_paired_sequence_by_truncation(v, first_chain_vtrim, first_chain_rtrim,
                                                               second_chain_vtrim, second_chain_rtrim, sep)
            new_seqs[k] = new_s
        self._sequences = new_seqs

    def _curate_paired_sequence_by_truncation(self, seq, first_chain_vtrim, first_chain_rtrim,
                                              second_chain_vtrim, second_chain_rtrim, sep):
        parts = seq.split(sep)
        s1=parts[0]
        s2=parts[1]
        s1 = s1[first_chain_vtrim:len(s1)-first_chain_rtrim]
        s2 = s2[second_chain_vtrim:len(s2) - second_chain_rtrim]
        out = s1+sep+s2
        return out

# Examples from EXPLORER library vs Gørils sanger-sequences PRAME-specific seqs.
# >r0
# DIQLTQSPSTLSASVGDRVTITCRASQGLSNWLAWYQQKPGEAPKLLIYAASTLQSGVPSRFSGSGSGTEFTLTISSLQPDDFATYYCLQYNSRSRALTFGGGTKVEIK:QVQLVQSGAEVKKPGASVKVSCKASGYTFTSYAMHWVRQAPGQRLEWMGWINAGNGNTKYSQKFQGRVTITRDTSASTVYIELSSLTSEDTAVYYCARAQQNTSWYDWFDPWGQGTLVTVSS
# >prame
# DIQVTQSPSSLSASVGDRVTITCQASQDISNYLNWYQQKPGKAPKLLIYDASNLETGVPSRFSGSGSGTDFTFTISSLQPEDIATYYCLQHNSYLPTFGGGTKVEIK:    QLVQSGAEVKKPGSSVKVSCKASPEAWSTFWISWVRQAPGQGLEWMGGIIPIFGTANYAQKFQGRVTITADESTSTAYMELSSLRSEDTAVYYCARDGYNYGQFDYWGQGTLVTVSS
#
# >9de50f9d-5a98-469b-be32-312576e3d1e9
# AIQMTQSPSSVSASVGDRVTITCQASQDISNYLNWYQQKPGKAPKLLIYDASNLETGVPSRFSGSGSGTDFTFTISSLQPEDIATYYCQQYDILLTFGGGTKVEIK:  QV QLVQSGSELKKPGASVRVSCKASGYSFTSYSMNWVRQAPGQGLEWMGWINTNTGNPTYAQGFTGRFVFSLDTSVSTAYLQISSLKPEDTAVYYCARGDTNSWSKENYWGQGTLVTVSS
# >A1-A11-ColE1_fwd2_A21_1_1-297
# DIQVTQSPSSLSASVGDRVTITCQASQDISNYLNWYQQKPGKAPKLLIYDASNLETGVPSRFSGSGSGTDFTFTISSLQPEDIATYYCLQHNSYLPTFGGGTKVEIK:    QLVQSGAEVKKPGSSVKVSCKASGGTFSSYAISWVRQAPGQGLEWMGGIIPIFGTANYAQKFQGRVTITADESTSTAYMELSSLRSEDTAVYYCARTIGHDLPDAFDIWGQGTMVTVSS
# Ergo:
# ->chop 4 first_chain_1 on both
# ->chop 2 first_chain2 on r0
#
# fn="C:/Nextera/div/ab_roberta/EXPLORER/r0_n1000.txt"
# seqs=CuratingAaSequenceMap(fn)
# seqs.curate_paired_sequences_by_truncation(4,0,0,0)
# seqs.write("C:/Nextera/div/ab_roberta/EXPLORER/curated/r0_n1000.txt")
#
# fn="C:/Nextera/div/ab_roberta/EXPLORER/r0.txt"
# seqs=CuratingAaSequenceMap(fn)
# seqs.curate_paired_sequences_by_truncation(4,0,2,0)
# seqs.write("C:/Nextera/div/ab_roberta/EXPLORER/curated/r0.txt")



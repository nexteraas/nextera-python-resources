from aa_sequence_map import AaSequenceMap


class SequenceMerger(object):
    def __init__(self, seq1, seq2):
        self._merged_seq=self._merge(seq1, seq2)

    def _merge(self, seq1, seq2):
        l = max(len(seq1), len(seq2))
        out=''
        for i in range(0,l,2):
            s1 = self._safe_char_at_check(seq1, i, '')
            if s1 == '':
                s1 = self._safe_char_at_check(seq2, i, '')
            s2 = self._safe_char_at_check(seq2, i+1, '')
            if s2 == '':
                s2 = self._safe_char_at_check(seq1, i+1, '')
            out+=s1+s2
        return out

    def _safe_char_at_check(self, s: str, index: int, default):
        if 0 <= index < len(s):
            return s[index]
        else:
            return default

    def get_merged_sequence(self):
        return self._merged_seq


class AaSequenceMapMerger(object):
    def __init__(self, aa_seq_map, sep_char=':'):
        map1, map2 = self._split(aa_seq_map, sep_char)
        self._merged_seqs = self._merge(map1, map2)

    def _split(self, aa_seq_map, sep_char=':'):
        map1 = {}
        map2 = {}
        for key, value in aa_seq_map.get_sequences().items():
            x=value.split(sep_char)
            map1[key]=x[0]
            map2[key]=x[1]
        out1 = AaSequenceMap(fn=aa_seq_map.get_fn(),sequences=map1, remove_gaps=aa_seq_map.get_remove_gaps(),
                             productive_only=aa_seq_map.get_productive_only(),tag=aa_seq_map.get_tag())
        out2 = AaSequenceMap(fn=aa_seq_map.get_fn(), sequences=map2, remove_gaps=aa_seq_map.get_remove_gaps(),
                             productive_only=aa_seq_map.get_productive_only(), tag=aa_seq_map.get_tag())
        return out1, out2

    def _merge(self, map1, map2):
        out= {}
        keys1 = list(map1.get_sequences().keys())
        keys2 = list(map2.get_sequences().keys())
        for i in range(0,len(map1.get_sequences())):
            k1=keys1[i]
            k2=keys2[i]
            merger=SequenceMerger(map1.get_sequences()[k1],map2.get_sequences()[k2])
            out[k1]=merger.get_merged_sequence()
        out = AaSequenceMap(fn=map1.get_fn(), sequences=out, remove_gaps=map1.get_remove_gaps(),
                             productive_only=map1.get_productive_only(), tag=map1.get_tag())
        return out

    def get_merged_sequences(self):
        return self._merged_seqs

class SequenceSanityChecker(object):
    def __init__(self, aa_sequence_maps):
        self._aa_sequence_maps = aa_sequence_maps

    def check_aas(self, canonicals_only=True):
        if canonicals_only:
            alphabet = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S',
                        'T', 'V', 'W', 'Y']
        else:
            alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for aa_sequence_map in self._aa_sequence_maps:
            for key in aa_sequence_map.get_sequences().keys():
                sequence=aa_sequence_map.get_sequences().get(key)
                for aa in sequence:
                    if aa not in alphabet:
                        raise Exception(f"Sequence {key} contains illegal character(s): '{aa}'; {sequence} ")

    def check_unique_aa_counts(self, position_from, position_to=None, aa_sequence_map=None):
        counter={}
        if aa_sequence_map is None:
            for aa_map in self._aa_sequence_maps:
                self._check_unique_aa_counts(position_from, position_to, aa_map, counter)
        else:
            self._check_unique_aa_counts(position_from, position_to, aa_sequence_map, counter)
        return counter

    def _check_unique_aa_counts(self, position_from, position_to, aa_sequence_map, counter):
        for sequence in aa_sequence_map.get_sequences().values():
            if position_to is None:
                subseq = sequence[position_from:]
            else:
                subseq = sequence[position_from:position_to]
            c = counter.get(subseq)
            if c is None:
                c=0
                counter[subseq] = c
            new_c=c+1
            counter[subseq]=new_c

    def get_max_lengths(self, aa_sequence_map=None):
        out=0
        if aa_sequence_map is None:
            for aa_map in self._fasta_importers:
                tmp = self._check_max_lengths(aa_map)
                if tmp >out:
                    out = tmp
        else:
            out = self._check_max_lengths(aa_sequence_map)
        return out

    def _check_max_lengths(self, aa_sequence_map):
        out=0
        for sequence in aa_sequence_map.get_sequences().values():
            if out<len(sequence):
                out=len(sequence)
        return out

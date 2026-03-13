class Counter(object):
    def __init__(self):
        self._value=0

    def add(self, number=1):
        self._value += number

    def get_value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class SequenceSanityChecker(object):
    def __init__(self, aa_sequence_maps):
        self._aa_sequence_maps = aa_sequence_maps

    def check_motif(self, motif, multiple_occurrences_only=False):
        out={}
        for aa_sequence_map in self._aa_sequence_maps:
            for key in aa_sequence_map.get_sequences().keys():
                aa_key = aa_sequence_map.get_tag()
                sequence = aa_sequence_map.get_sequences().get(key)
                c=sequence.count(motif)
                b=False
                if multiple_occurrences_only:
                    if c>1:
                        b=True
                else:
                    if c>0:
                        b=True
                if b:
                    aa_c=out.get(aa_key)
                    if aa_c is None:
                        aa_c=0
                    aa_c+=1
                    out[aa_key]=aa_c
            if out.get(aa_key) is None:
                out[aa_key]=0
            else:
                out[aa_key]=out[aa_key]/len(aa_sequence_map.get_sequences())
        return out

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

    def get_seq_lengths(self, aa_sequence_map=None):
        if aa_sequence_map is None:
            out={}
            for aa_map in self._aa_sequence_maps:
                avg, max = self._get_seq_lengths(aa_map)
                out[aa_map.get_tag()] = [avg, max]
        else:
            avg, max = self._get_seq_lengths(aa_sequence_map)
        return avg, max

    def _get_seq_lengths(self, aa_sequence_map):
        max=0
        avg=0
        for sequence in aa_sequence_map.get_sequences().values():
            l = len(sequence)
            avg+=l
            if max<l:
                max=l
        avg=avg/len(aa_sequence_map.get_sequences())
        return avg, max

    def get_duplicates(self, aa_sequence_map=None):
        out = {}
        if aa_sequence_map is None:
            for aa_map in self._aa_sequence_maps:
                tmp = self._get_duplicates(aa_map)
                out[aa_map.get_tag()] = tmp
        else:
            out = self._get_duplicates(aa_sequence_map)
        return out

    def _get_duplicates(self, aa_sequence_map):
        tmp={}
        for key, sequence in aa_sequence_map.get_sequences().items():
            if tmp.get(sequence) is not None:
                pass
            tmp[sequence] = key
        c1 = len(aa_sequence_map.get_sequences())
        c2 = len(tmp)
        return c1-c2

    def check_aa_composition(self, aa_sequence_map=None):
        out = {}
        if aa_sequence_map is None:
            for aa_map in self._aa_sequence_maps:
                tmp = self._check_aa_composition(aa_map)
                out[aa_map.get_tag()]=tmp
        else:
            out = self._check_aa_composition(aa_sequence_map)
        return out

    def _check_aa_composition(self, aa_sequence_map):
        out={}
        tot = 0
        for sequence in aa_sequence_map.get_sequences().values():
            for aa in sequence:
                tot += 1
                c=out.get(aa)
                if c is None:
                    c=Counter()
                    out[aa]=c
                c.add()
        sorted_items = sorted(out.items(), key=lambda item: item[1]._value)
        out = dict(sorted_items)
        for key, value in out.items():
            out[key]=value.get_value() / tot
        return out

    def create_std_report(self):
        out='Sanity checker report:\n'
        out += 'Tags:\n'
        for aa_map in self._aa_sequence_maps:
            out += str(aa_map.get_tag()) + ': ' + str(aa_map.get_fn()) + '\n'
        out+='Checking legal Aas...\n'
        self.check_aas()
        out+='Done!\n'
        out+='Checking sequences lengths:\n'
        for aa_map in self._aa_sequence_maps:
            avg, max= self.get_seq_lengths(aa_map)
            out+=str(aa_map.get_tag()) + ': ' + str(avg) + '; ' + str(max) + '\n'
        out += 'Checking duplicates:\n'
        for aa_map in self._aa_sequence_maps:
            dup = self.get_duplicates(aa_map)
            out += str(aa_map.get_tag()) + ': ' + str(dup) + '\n'
        out += 'Checking sequences Aa counts, -2 to end:\n'
        for aa_map in self._aa_sequence_maps:
            aacount = self.check_unique_aa_counts(position_from=-2, position_to=None, aa_sequence_map=aa_map)
            out+=str(aa_map.get_tag()) + ': ' + str(aacount) + '\n'
        for key, value in aacount.items():
            out+=str(key) + ': ' + str(value) + '\n'
        out += 'Checking sequences Aa motif "CAR":\n'
        single_occ = self.check_motif('CAR')
        for key, value in single_occ.items():
            out+=str(key) + ': ' + str(value) + '\n'
        out += 'Checking sequences Aa motif "WG":\n'
        single_occ = self.check_motif('WG')
        for key, value in single_occ.items():
            out+=str(key) + ': ' + str(value) + '\n'
        out += 'Checking sequences Aa motif "TVSS":\n'
        single_occ = self.check_motif('TVSS')
        for key, value in single_occ.items():
            out+=str(key) + ': ' + str(value) + '\n'
        out += 'Checking sequences Aa motif "CQQ":\n'
        single_occ = self.check_motif('CQQ')
        for key, value in single_occ.items():
            out += str(key) + ': ' + str(value) + '\n'
        out += 'Checking sequences Aa motif "FG":\n'
        single_occ = self.check_motif('FG')
        for key, value in single_occ.items():
            out += str(key) + ': ' + str(value) + '\n'
        out += 'Checking sequences Aa motif "KVEIK":\n'
        single_occ = self.check_motif('KVEIK')
        for key, value in single_occ.items():
            out += str(key) + ': ' + str(value) + '\n'
        out += 'Checking sequences Aa compositions:\n'
        composition = self.check_aa_composition()
        for key, value in composition.items():
            out+=str(key) + ': '
            for i in range(len(value)-1,0,-1):
                k = list(value.keys())[i]
                comp = value.get(k)
                out+=k + ':' + str(comp)+ '; '
            out+='\n'

        return out
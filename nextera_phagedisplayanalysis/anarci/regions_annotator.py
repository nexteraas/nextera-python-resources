class RegionsAnnotator(object):
    def __init__(self, scheme):
        self._scheme = scheme

    def annotate(self, aa_numbering, chain=1):
        aa_numbering_s = str(aa_numbering)
        aa_number=self._get_aa_number(aa_numbering_s)
        if self._scheme=='imgt':
            return self._get_imgt_region(aa_number, chain)
        elif self._scheme=='kabat':
            return self._get_kabat_region(aa_number, chain, aa_numbering_s)
        elif self._scheme=='chothia':
            return self._get_chothia_martin_region(aa_number, chain)

    def _get_aa_number(self, aa_numbering):
        for i in range(len(aa_numbering), 0, -1):
            c = aa_numbering[i-1 : i]
            if c.isnumeric():
                return int(aa_numbering[0 : i])

    def _get_imgt_region(self, aa_number, chain):
        out = ''
        if aa_number<27:
            out = "FR1"
        elif aa_number<39:
            out = "CDR1"
        elif aa_number<56:
            out = "FR2"
        elif aa_number<66:
            out = "CDR2"
        elif aa_number<105:
            out = "FR3"
        elif aa_number<118:
            out = "CDR3"
        else:
            out = '-'
        if chain==1:
            if aa_number >= 36 and aa_number <= 42:
                out += '(c)'
            elif aa_number >= 52 and aa_number <= 68:
                out += '(c)'
            elif aa_number >= 105 and aa_number <= 116:
                out += '(c)'
        else:
            if aa_number >= 35 and aa_number <= 40:
                out += '(c)'
            elif aa_number >= 52 and aa_number <= 66:
                out += '(c)'
            elif aa_number >= 105 and aa_number <= 116:
                out += '(c)'
        return out

    def _get_kabat_region(self, aa_number, chain, aa_numbering):
        out = ''
        if chain == 1:
            if aa_number < 24:
                out = "FR1"
            elif aa_number < 35:
                out = "CDR1"
            elif aa_number < 50:
                out = "FR2"
            elif aa_number < 57:
                out = "CDR2"
            elif aa_number < 89:
                out = "FR3"
            elif aa_number < 98:
                out = "CDR3"
            else:
                out = '-'
        else:
            if aa_number < 31:
                out =  "FR1"
            elif aa_number < 35:
                out = "CDR1"
            elif aa_number==35:
                if aa_numbering.endswith('35'):
                    out = "CDR1"
                elif aa_numbering.endswith('A') or aa_numbering.endswith('B'):
                    out = "CDR1"
                else:
                    out = "FR2"
            elif aa_number < 50:
                out = "FR2"
            elif aa_number < 66:
                out = "CDR2"
            elif aa_number < 95:
                out = "FR3"
            elif aa_number < 103:
                out = "CDR3"
            else:
                out = '-'
        return out

    def _get_chothia_martin_region(self, aa_number, chain):
        out=''
        if chain==1:
            if aa_number<26:
                out = "FR1"
            elif aa_number<33:
                out = "CDR1"
            elif aa_number<50:
                out = "FR2"
            elif aa_number<53:
                out = "CDR2"
            elif aa_number<91:
                out = "FR3"
            elif aa_number<97:
                out = "CDR3"
            else:
                out = '-'
            if aa_number>=30 and aa_number<=36:
                out+='(c)'
            elif aa_number >= 46 and aa_number <= 55:
                    out += '(c)'
            elif aa_number >= 89 and aa_number <= 96:
                out += '(c)'
        else:
            if aa_number < 26:
                out = "FR1"
            elif aa_number < 33:
                out = "CDR1"
            elif aa_number < 52:
                out = "FR2"
            elif aa_number < 57:
                out = "CDR2"
            elif aa_number < 96:
                out = "FR3"
            elif aa_number < 102:
                out = "CDR3"
            else:
                out = '-'
            if aa_number >= 30 and aa_number <= 35:
                out += '(c)'
            elif aa_number >= 47 and aa_number <= 58:
                out += '(c)'
            elif aa_number >= 93 and aa_number <= 101:
                out += '(c)'
        return out

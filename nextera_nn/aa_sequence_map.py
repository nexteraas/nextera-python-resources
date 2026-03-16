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

    def get_sequence_list(self):
        out=[]
        for s in self._sequences.values():
            out.append(s)
        return out

    def remove_sequences(self, disallowed_aas=[]):
        disallowed_aas = [aa.upper() for aa in disallowed_aas]
        keys_to_remove = [key for key, value in self._sequences.items() if
                          self._contains_any_char(value, disallowed_aas)]
        for key in keys_to_remove:
            del self._sequences[key]
        return len(keys_to_remove)

    def _contains_any_char(self, target_string, char_list):
        return any(char in target_string for char in char_list)

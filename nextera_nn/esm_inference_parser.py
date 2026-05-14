class Parser():
    def __init__(self, data):
        self._data = data

    def head(self, n=10):
        out = ""
        i=0
        for r in self._data:
            out+=str(r) + "\n"
            print(r)
            if n is not None:
                if i>=n:
                    break
            i+=1
        return out

    def filter(self, class_txt, threshold=0.5, above=True):
        i = -1
        out=[]
        for r in self._data:
            i+=1
            txt= r['label']
            if class_txt == txt:
                val = r['score']
                if above:
                    if val >= threshold:
                        r['index'] = i
                        out.append(r)
                else:
                    if val <= threshold:
                        r['index'] = i
                        out.append(r)
        return out

    def __str__(self):
        out = str(len(self._data)) +  ' items'
        return out

import pickle
from esm_inference_parser import Parser

# Loading (Unpickling)
with open("C:/Nextera/div/ab_roberta/EXPLORER/curated/results/r0_result.pkl", "rb") as f:
    loaded_data = pickle.load(f)

print(len(loaded_data))

p=Parser(loaded_data)
#print(p.head(n=100))
p=p.filter('LABEL_0', 0.0, True)
p=Parser(p)
print(str(p))

exit(0)
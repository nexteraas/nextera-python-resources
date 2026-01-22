import os
import csv
import pandas as pd
from nextera_utils.docker_interop import DockerInterop


class AbpredParser:
    def __init__(self, path, platform_map):
        self._path = path
        self._platform_map = {value: key for key, value in platform_map.items()}

    def run(self, out_fn):
        print('running parser...')
        results = []
        f = os.path.join(self._path, 'abpred-ACCSTAB-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-ACSINS-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-BVPELISA-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-CIC-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-CSIBLI-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-DSF-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-ELISA-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-HEK-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-HIC-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-PSR-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-SGAC-predictions.csv')
        self._read_file(f, results)
        f = os.path.join(self._path, 'abpred-SMAC-predictions.csv')
        self._read_file(f, results)
        df = pd.DataFrame(results, columns=['Ab', 'Platform', 'Prediction'])
        docker=DockerInterop.get_instance()
        docker.write_csv(df, out_fn)

    def _read_file(self, fn, results):
        print('parsing...')
        with open(fn, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)#, skipinitialspace=True)
            next(reader, None)  # Skip the first row (header)
            for row in reader:
                val=self._platform_map.get(row[1])
                if val is not None:
                    row[1] = val
                    print('changed...')
                results.append(row)

    # def _parse_file(self, file_content, platform, results):
    #     out={}
    #     lines_list = file_content.splitlines()
    #     for line in lines_list:
    #         fields = line.split('\t')
    #         out[fields[0]]=fields[2]
    #     results[platform] = out

# abpred_seq_composition.txt
# abpred_table_composition.csv
#
# platform_map = {}
# platform_map['AS']='ACCSTAB'
# platform_map['AC'] = 'ACSINS'
# platform_map['BVP'] = 'BVPELISA'
# platform_map['CSI'] = 'CSIBLI'
# x=AbpredParser('C:/docker_data_exchange/out/0ef4dd00-9f2e-448b-88f6-3d6318546a38', platform_map)
# x.run('')
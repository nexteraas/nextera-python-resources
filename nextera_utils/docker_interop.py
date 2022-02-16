import csv

import pandas as pd


class DockerInterop:
    _INPUT_HEADER_PREFIX = "input_fn_"
    _OUTPUT_HEADER_PREFIX = "output_fn_"
    _ARGS_FN = "arguments.csv"
    _EXCEPTION_FN = "exception.txt"
    _PROGRESS_FN = "progress.txt"
    _DATA_EXCHANGE_IN_DIR = "/data_exchange/in/"
    _DATA_EXCHANGE_OUT_DIR = "/data_exchange/out/"
    _DEBUG_DATA_EXCHANGE_IN_DIR = "C:/docker_data_exchange/in/"
    _DEBUG_DATA_EXCHANGE_OUT_DIR = "C:/docker_data_exchange/out/"
    _INSTANCE = None

    @staticmethod
    def get_instance():
        if DockerInterop._INSTANCE is None:
            raise Exception('Not instantiated')
        return DockerInterop._INSTANCE

    def __init__(self, args_fn, debug_key=None):
        self._args = self.read_csv(args_fn)
        self._debug_key = debug_key
        DockerInterop._INSTANCE = self

    def get_debug_key(self):
        return self._debug_key

    def read_csv(self, fn, index_col=None):
        df = pd.read_csv(fn, sep='\t', index_col=index_col)
        return df

    def get_input_filenames(self):
        columns = self._args.columns.to_list()
        out = []
        for col in columns:
            if col.startswith(DockerInterop._INPUT_HEADER_PREFIX):
                filename = self._args[col].iloc[0]
                if not self._debug_key is None:
                    filename = self._create_debug_fn(filename)
                out.append(filename)
        return out

    def get_output_filenames(self):
        columns = self._args.columns.to_list()
        out=[]
        for col in columns:
            if col.startswith(DockerInterop._OUTPUT_HEADER_PREFIX):
                filename = self._args[col].iloc[0]
                if not self._debug_key is None:
                    filename = self._create_debug_fn(filename)
                out.append(filename)
        return out

    def _create_debug_fn(self, fn):
        if fn.startswith(DockerInterop._DATA_EXCHANGE_IN_DIR):
            path = DockerInterop._DEBUG_DATA_EXCHANGE_IN_DIR + self._debug_key + '/'
            out = fn.replace(DockerInterop._DATA_EXCHANGE_IN_DIR, path)
        elif fn.startswith(DockerInterop._DATA_EXCHANGE_OUT_DIR):
            path = DockerInterop._DEBUG_DATA_EXCHANGE_OUT_DIR + self._debug_key + '/'
            out = fn.replace(DockerInterop._DATA_EXCHANGE_OUT_DIR, path)
        return out

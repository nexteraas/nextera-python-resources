import ntpath
import pandas as pd
from numpy.testing._private.parameterized import param


class DockerInterop:
    _INPUT_HEADER_PREFIX = "input_fn_"
    _INPUT_TAGS_HEADER_PREFIX = "input_fn_tags"
    _OUTPUT_HEADER_PREFIX = "output_fn_"
    _INFOS_HEADER_PREFIX = "info_"
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
        self._input_fn_tags = self._load_input_fn_tags()
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
            if self._is_input_header_column(col):
                filename = self._args[col].iloc[0]
                if self._debug_key is not None:
                    filename = self._create_debug_fn(filename)
                out.append(filename)
        return out

    def get_output_filenames(self):
        columns = self._args.columns.to_list()
        out = []
        for col in columns:
            if self._is_output_header_column(col):
                filename = self._args[col].iloc[0]
                if self._debug_key is not None:
                    filename = self._create_debug_fn(filename)
                out.append(filename)
        return out

    def _load_input_fn_tags(self):
        out = {}
        columns = self._args.columns.to_list()
        for col in columns:
            if col == DockerInterop._INPUT_TAGS_HEADER_PREFIX:
                s = self._args[col].iloc[0]
                s = s.split('\t')
                for i in range(0, len(s), 2):
                    fn = self._get_filename(s[i])
                    tag = s[i+1]
                    out[fn] = tag
        return out

    def get_tag(self, fn):
        for key in self._input_fn_tags:
            if fn.endswith(key):
                return self._input_fn_tags[key]
        return None

    def _get_filename(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def get_infos(self):
        out={}
        columns = self._args.columns.to_list()
        for col in columns:
            if self._is_info_header_column(col):
                key=col[len(DockerInterop._INFOS_HEADER_PREFIX):]
                s = self._args[col].iloc[0]
                s = s.split('\t')
                out[key]  = s
        return out

    def get_info(self, index):
        columns = self._args.columns.to_list()
        for col in columns:
            if col == DockerInterop._INFOS_HEADER_PREFIX + str(index):
                s = self._args[col].iloc[0]
                s = s.split('\t')
                return s
        return None

    def get_info_value(self, index, key):
        info = self.get_info(index)
        if info is not None:
            for i in info:
                tmp = i.split('=')
                if len(tmp) == 2:
                    if tmp[0] == key:
                        return tmp[1]
        return None

    def _create_debug_fn(self, fn):
        if fn.startswith(DockerInterop._DATA_EXCHANGE_IN_DIR):
            path = DockerInterop._DEBUG_DATA_EXCHANGE_IN_DIR + self._debug_key + '/'
            out = fn.replace(DockerInterop._DATA_EXCHANGE_IN_DIR, path)
        elif fn.startswith(DockerInterop._DATA_EXCHANGE_OUT_DIR):
            path = DockerInterop._DEBUG_DATA_EXCHANGE_OUT_DIR + self._debug_key + '/'
            out = fn.replace(DockerInterop._DATA_EXCHANGE_OUT_DIR, path)
        return out

    def _is_input_header_column(self, col):
        if col==self._INPUT_TAGS_HEADER_PREFIX:
            return False
        s = self._get_string_before_last_underscore(col)
        return s == DockerInterop._INPUT_HEADER_PREFIX

    def _is_output_header_column(self, col):
        s = self._get_string_before_last_underscore(col)
        return s == DockerInterop._OUTPUT_HEADER_PREFIX

    def _is_info_header_column(self, col):
        s = self._get_string_before_last_underscore(col)
        return s == DockerInterop._INFOS_HEADER_PREFIX

    def _get_string_before_last_underscore(self, s):
        index = s.rfind('_')
        if index == -1:
            return ''
        out = s[:index + 1]
        return out

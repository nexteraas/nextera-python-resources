import ntpath
import pandas as pd
import numpy as np
import os


class DockerInterop:
    _DATA_ITEM_HEADER_PREFIX = 'data_'
    _INFOS_HEADER_PREFIX = "info_"
    _ARGS_FN = "arguments.csv"
    _EXCEPTION_FN = "exception.txt"
    _PROGRESS_FN = "progress.txt"
    _DATA_EXCHANGE_IN_DIR = "/data_exchange/in/"
    _DATA_EXCHANGE_OUT_DIR = "/data_exchange/out/"
    _DEBUG_DATA_EXCHANGE_IN_DIR = "C:/docker_data_exchange/in/"
    _DEBUG_DATA_EXCHANGE_OUT_DIR = "C:/docker_data_exchange/out/"
    _TMP_DIR="/tmp/"
    _INSTANCE = None

    @staticmethod
    def get_instance():
        if DockerInterop._INSTANCE is None:
            raise Exception('Not instantiated')
        return DockerInterop._INSTANCE

    def __init__(self, args_fn, debug_key=None):
        if args_fn is not None:
            self._args = self.read_csv(args_fn)
        self._debug_key = debug_key
        DockerInterop._INSTANCE = self

    def get_debug_key(self):
        return self._debug_key

    def read_csv(self, fn, index_col=None, na_values=None):
        if na_values is None:
            df = pd.read_csv(fn, sep='\t', index_col=index_col, keep_default_na=False)
        else:
            df = pd.read_csv(fn, sep='\t', index_col=index_col, na_values = na_values)
        return df

    # def _convert_columns_to_numerical(self, df, nan_to_none=True):
    #     cols = []
    #     for col in df:
    #         isNum = True
    #         for row in df[col]:
    #             if row:
    #                 try:
    #                     x = float(row)
    #                 except:
    #                     isNum = False
    #                     break
    #         if isNum:
    #             cols.append(col)
    #     for col in cols:
    #         df[col] = pd.to_numeric(df[col], errors='coerce')
    #     if nan_to_none:
    #         for col in cols:
    #             df[col] = df[col].replace({np.nan: None})
    #     return df

    def get_data_items(self):
        out = []
        columns = self._args.columns.to_list()
        for col in columns:
            if self._is_data_item_column(col):
                in_fn = self._args[col].iloc[0]
                out_fig_fn = self._args[col].iloc[1]
                out_tbl_fn = self._args[col].iloc[2]
                if self._debug_key is not None:
                    in_fn = self._create_debug_fn(in_fn)
                    out_fig_fn = self._create_debug_fn(out_fig_fn)
                    out_tbl_fn = self._create_debug_fn(out_tbl_fn)
                tag = self._args[col].iloc[3]
                out.append((in_fn, out_fig_fn, out_tbl_fn, tag))
        return out

    def _get_filename(self, path):
        return DockerInterop.get_filename(path, True)

    @staticmethod
    def get_filename(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @staticmethod
    def get_filename_parts(filename):
        fn, fn_ext = os.path.splitext(filename)
        return fn, fn_ext

    def get_infos(self):
        out={}
        columns = self._args.columns.to_list()
        for col in columns:
            if self._is_info_header_column(col):
                key=col[len(DockerInterop._INFOS_HEADER_PREFIX):]
                s = self._args[col].iloc[0]
                if s == s:
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
        if fn.strip()=='':
            return ''
        if fn.startswith(DockerInterop._DATA_EXCHANGE_IN_DIR):
            path = DockerInterop._DEBUG_DATA_EXCHANGE_IN_DIR + self._debug_key + '/'
            out = fn.replace(DockerInterop._DATA_EXCHANGE_IN_DIR, path)
        elif fn.startswith(DockerInterop._DATA_EXCHANGE_OUT_DIR):
            path = DockerInterop._DEBUG_DATA_EXCHANGE_OUT_DIR + self._debug_key + '/'
            out = fn.replace(DockerInterop._DATA_EXCHANGE_OUT_DIR, path)
        return out

    def _is_data_item_column(self, col):
        if col=='data_exchange':
            return False
        s = self._get_string_before_last_underscore(col)
        return s == DockerInterop._DATA_ITEM_HEADER_PREFIX

    def _is_info_header_column(self, col):
        s = self._get_string_before_last_underscore(col)
        return s == DockerInterop._INFOS_HEADER_PREFIX

    def _get_string_before_last_underscore(self, s):
        index = s.rfind('_')
        if index == -1:
            return ''
        out = s[:index + 1]
        return out

    @staticmethod
    def parse_java_boolean(b):
        if b == 'true':
            return True
        elif b == 'false':
            return False
        else:
            raise ValueError('Could not parse Java boolean')

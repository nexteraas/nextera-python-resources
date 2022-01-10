from _ast import stmt
from builtins import property
import time
import pandas as pd
import sys
import uuid
import os


class DockerInterop:
    _ARGS_FN='args.txt'
    _EXPORT_FN = 'export_filename'
    _IMPORT_FN = 'import_filename'
    _PROGRESS_FN = 'progress_filename'
    _EXCEPTION_FN = 'exception_filename'

    def __init__(self):
        self._data_exchange_folder="/data_exchange"
        if not os.path.isdir(self._data_exchange_folder):
            self._data_exchange_folder = "/mnt/c/temp/docker_interop"
        if not os.path.isdir(self._data_exchange_folder):
            self._data_exchange_folder = "C:/temp/docker_interop"

    def _get_data_exchange_folder_in(self):
        out=os.path.join(self._data_exchange_folder, 'in')
        return out

    def _get_data_exchange_folder_out(self):
        out=os.path.join(self._data_exchange_folder, 'out')
        return out

    def get_input_fn(self, fn):
        return os.path.join(self._get_data_exchange_folder_in(), fn)

    def get_output_fn(self, fn):
        return os.path.join(self._get_data_exchange_folder_out(), fn)

    def read_df(self, fn):
        df = pd.read_csv(fn, sep='\t')
        return df

    def get_args(self):
        df =self.read_df(self.get_input_fn(DockerInterop._ARGS_FN))
        out=df.to_dict(orient='records')
        return out[0]
    # def _parse_args(self):
    #     args_fn = sys.argv[1]
    #     out = pd.read_csv(args_fn, sep='\t')
    #     return out
    #
    # def read_data(self, index=None, index_col=None):
    #     data_fn = self.get_data_fn(index)
    #     if data_fn is None: return None, None
    #     out = pd.read_csv(data_fn, sep='\t', index_col=index_col)
    #     return data_fn, out
    #
    # def get_data_fn(self, index=None):
    #     s = DockerInterop._EXPORT_FN
    #     if index is not None:
    #         s = s + str(index)
    #     if s in self._args.columns:
    #         out = self._args[s][0]
    #     else:
    #         out = None
    #     return out
    #
    # def write_progress(self, value, comment):
    #     progress_fn = self._get_progress_fn()
    #     data = {'value': [value], 'comment': [comment]}
    #     prog_df = pd.DataFrame.from_dict(data)
    #     prog_df.astype({'value': 'float'})
    #     path = os.path.dirname(progress_fn)
    #     tmp_fn = os.path.join(path, str(uuid.uuid4()))
    #     prog_df.to_csv(tmp_fn, index=False, sep='\t')
    #     for i in range(0, 10):
    #         if os.path.exists(progress_fn):
    #             try:
    #                 time.sleep(1)
    #                 os.remove(progress_fn)
    #             except:
    #                 pass
    #     os.rename(tmp_fn, progress_fn)
    #
    # def write_data(self, df, index=None):
    #     output_fn = self._get_output_fn(index=None)
    #     df.to_csv(output_fn, index=False, sep='\t')
    #
    # def write_exception(self, msg):
    #     exc_fn = self._get_exception_fn()
    #     path = os.path.dirname(exc_fn)
    #     tmp_fn = os.path.join(path, str(uuid.uuid4()))
    #     f = open(tmp_fn, 'w')
    #     f.write(str(msg))
    #     f.close()
    #     os.rename(tmp_fn, exc_fn)
    #
    # def _get_progress_fn(self):
    #     out = self._args[DockerInterop._PROGRESS_FN][0]
    #     return out
    #
    # def _get_exception_fn(self):
    #     out = self._args[DockerInterop._EXCEPTION_FN][0]
    #     return out
    #
    # def _get_output_fn(self, index=None):
    #     s = DockerInterop._IMPORT_FN
    #     if index is not None:
    #         s = s + str(index)
    #     out = self._args[s][0]
    #     return out


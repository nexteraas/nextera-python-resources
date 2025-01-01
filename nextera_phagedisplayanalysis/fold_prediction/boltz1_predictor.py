import os
import shutil
from nextera_utils.docker_interop import DockerInterop
from click.testing import CliRunner


class Boltz1Predictor(object):
    def __init__(self, in_fn, accelerator='cpu', devices=1,output_format='mmcif', num_workers=2):
        self._in_path = self._format_in_file(in_fn)
        self._in_fn = DockerInterop.get_filename(self._in_path)
        self._in_fn, self._in_fn_ext = DockerInterop.get_filename_parts(self._in_fn)
        self._accelerator = accelerator
        self._devices = devices
        self._output_format = output_format
        self._num_workers = num_workers

    def _format_in_file(self, in_fn):
        path, ext = DockerInterop.get_filename_parts(in_fn)
        dest_fn=path + '.fasta'
        shutil.copy(in_fn, dest_fn)
        return dest_fn

    # def _set_out_dir(self, in_fn):
    #     out = os.path.dirname(os.path.realpath(in_fn))
    #     return out

    def predict(self, out_fn):
        import boltz.main as bm
        runner = CliRunner()
        args = []
        args.append('predict')
        args.append(self._in_path)
        args.append('--out_dir')
        args.append(DockerInterop._TMP_DIR)
        args.append('--cache')
        args.append('/boltz/cache')
        args.append('--accelerator')
        args.append(self._accelerator)
        args.append('--devices')
        args.append(self._devices)
        args.append('--output_format')
        args.append(self._output_format)
        args.append('--num_workers')
        args.append(self._num_workers)
        args.append('--use_msa_server')
        print('Running boltz1 cmd...')
        result = runner.invoke(bm.cli, args)
        print('Boltz - result:')
        print(result)
        print(result.output)
        print('Moving out files...')
        self._move_out_files(out_fn)

    def _move_out_files(self, out_fn):
        src_dir= DockerInterop._TMP_DIR + 'boltz_results_' + self._in_fn + '/predictions/' + self._in_fn + '/'
        if self._output_format=='mmcif':
            src_prediction=src_dir + self._in_fn + '_model_0.cif'
        elif self._output_format=='pdb':
            src_prediction = src_dir + self._in_fn + '_model_0.pdb'
        print('Moving out files:' + src_prediction + ' - ' + out_fn)
        shutil.move(src_prediction, out_fn)
        print('Moving out files done.')



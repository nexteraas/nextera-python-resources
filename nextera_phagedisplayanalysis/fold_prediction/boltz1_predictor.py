import os
import shutil
from nextera_utils.docker_interop import DockerInterop
from click.testing import CliRunner
from numpy import load
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import nextera_utils.utils as utils


class Boltz1Predictor(object):
    def __init__(self, in_fn, input_format='fasta', accelerator='cpu', devices=1,output_format='mmcif', num_workers=2,
                 pae=True, pde=True, recycling_steps=3, sampling_steps=200, diffusion_samples=1,
                 step_scale=1.638, msa_pairing_strategy='greedy', use_msa_server=True, seed=None):
        self._input_format = input_format
        self._in_path = self._format_in_file(in_fn)
        self._in_fn = DockerInterop.get_filename(self._in_path)
        self._in_fn, self._in_fn_ext = DockerInterop.get_filename_parts(self._in_fn)
        self._accelerator = accelerator
        self._devices = devices
        self._output_format = output_format
        self._num_workers = num_workers
        self._pae = pae
        self._pde = pde
        self._use_msa_server = use_msa_server
        self._recycling_steps = recycling_steps
        self._sampling_steps = sampling_steps
        self._diffusion_samples = diffusion_samples
        self._step_scale = step_scale
        self._msa_pairing_strategy = msa_pairing_strategy
        self._seed = seed

    def _format_in_file(self, in_fn):
        path, ext = DockerInterop.get_filename_parts(in_fn)
        if self._input_format=='fasta':
            dest_fn=path + '.fasta'
        else:
            dest_fn = path + '.yaml'
        shutil.copy(in_fn, dest_fn)
        return dest_fn

    def predict(self, out_structure_fn,  out_confidence_fn,  out_pae_fn=None, out_pde_fn=None, out_plddt_fn=None):
        args = self._create_boltz_args()
        runner = CliRunner()
        import boltz.main as bm
        print('Running boltz1 cmd...')
        result = runner.invoke(bm.cli, args)
        print('Boltz - result:')
        print(result)
        print(result.output)
        print('Moving out files...')
        self._move_out_files(out_structure_fn, out_confidence_fn, out_pae_fn, out_pde_fn, out_plddt_fn)

    def _create_boltz_args(self):
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
        args.append('--recycling_steps')
        args.append(self._recycling_steps)
        args.append('--sampling_steps')
        args.append(self._sampling_steps)
        args.append('--diffusion_samples')
        args.append(self._diffusion_samples)
        # args.append('--step_scale')
        # args.append(self._step_scale)
        args.append('--msa_pairing_strategy')
        args.append(self._msa_pairing_strategy)
        if self._use_msa_server:
            args.append('--use_msa_server')
        if self._pae:
            args.append('--write_full_pae')
        if self._pde:
            args.append('--write_full_pde')
        if self._seed is not None:
            args.append('--seed')
            args.append(self._seed)
        return args

    def _move_out_files(self, out_structure_fn, out_confidence_fn, out_pae_fn, out_pde_fn, out_plddt_fn):
        src_dir= DockerInterop._TMP_DIR + 'boltz_results_' + self._in_fn + '/predictions/' + self._in_fn + '/'
        if self._output_format=='mmcif':
            src_prediction=src_dir + self._in_fn + '_model_0.cif'
        elif self._output_format=='pdb':
            src_prediction = src_dir + self._in_fn + '_model_0.pdb'
        print('Moving out files:' + src_prediction + ' - ' + out_structure_fn)
        shutil.move(src_prediction, out_structure_fn)

        src_dir = DockerInterop._TMP_DIR + 'boltz_results_' + self._in_fn + '/predictions/' + self._in_fn + '/'
        src_prediction = src_dir + 'confidence_' + self._in_fn + '_model_0.json'
        print('Moving out files:' + src_prediction + ' - ' + out_confidence_fn)
        shutil.move(src_prediction, out_confidence_fn)

        if out_pae_fn is not None:
            src_dir = DockerInterop._TMP_DIR + 'boltz_results_' + self._in_fn + '/predictions/' + self._in_fn + '/'
            src_prediction = src_dir + 'pae_' + self._in_fn + '_model_0.npz'
            print('Creating PAE file:' + src_prediction + ' - ' + out_pae_fn)
            self._parse_npz(src_prediction, out_pae_fn)
            print('PAE file created')

        if out_pde_fn is not None:
            src_dir = DockerInterop._TMP_DIR + 'boltz_results_' + self._in_fn + '/predictions/' + self._in_fn + '/'
            src_prediction = src_dir + 'pde_' + self._in_fn + '_model_0.npz'
            print('Creating PDE file:' + src_prediction + ' - ' + out_pde_fn)
            self._parse_npz(src_prediction, out_pde_fn)
            print('PDE file created')

        if out_plddt_fn is not None:
            src_dir = DockerInterop._TMP_DIR + 'boltz_results_' + self._in_fn + '/predictions/' + self._in_fn + '/'
            src_prediction = src_dir + 'plddt_' + self._in_fn + '_model_0.npz'
            print('Creating pLDDT file:' + src_prediction + ' - ' + out_plddt_fn)
            self._parse_npz(src_prediction, out_plddt_fn)
            print('pLDDT file created')

        print('Moving out files done.')

    def _parse_npz(self, in_fn, out_fn):
        data = load(in_fn)
        lst = data.files
        for item in lst:
            self._plot_npz_data(data[item], out_fn)

    def _plot_npz_data(self, data, out_fn):
        s = data.shape
        if len(s)==1:
            data = np.asarray(data).reshape(data.size, 1)
        plt.figure()
        ax = sns.heatmap(data)
        utils.saveFigure(out_fn)
        plt.show()


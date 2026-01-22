import subprocess
from nextera_utils.docker_interop import DockerInterop


class AbpredExecutor:
    def __init__(self, in_fn, abpred_parser):
        self._in_fn = in_fn
        self._abpred_parser = abpred_parser

    @staticmethod
    def get_out_dir():
        return '/abpred/host/abpred_outputs/'

    def run(self, predictions_out_fn):
        p = self._get_exe()
        abpred_ps = subprocess.Popen([p, self._in_fn], stdin=subprocess.PIPE, shell=False)
        stdout, stderr = abpred_ps.communicate()
        if stdout is not None:
            print('Abpred stdout:' + str(stdout))
        self._abpred_parser.run(predictions_out_fn)

    def _get_exe(self):
        debug_key = DockerInterop.get_instance().get_debug_key()
        if debug_key is None:
            return '/abpred/run_preds.sh'
        else:
            return 'docker run --rm -v $(pwd)/:/abpred/host maxhebditch/abpred'

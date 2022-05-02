import subprocess
from os.path import exists
from statistics import stdev


class CircosExecutor:

    @staticmethod
    def execute_circos(label_size, in_fn, out_fn):
        circos_fn = "/circos-0.69-9/tools/tableviewer/exec_circos.sh"
        circos_ps = subprocess.Popen([circos_fn, label_size, in_fn,  out_fn], stdin=subprocess.PIPE, shell=False)
        stdout, stderr = circos_ps.communicate()
        if stdout is not None:
            print('CIRCOS stdout:' + str(stdout))



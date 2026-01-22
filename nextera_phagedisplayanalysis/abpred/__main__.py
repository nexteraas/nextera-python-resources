from pathlib import Path
import os
from nextera_phagedisplayanalysis.abpred import abpred_parser as ap
from nextera_phagedisplayanalysis.abpred import abpred_executor as ae
from nextera_phagedisplayanalysis.abpred import benchmark as b
from nextera_phagedisplayanalysis.abpred import ranks as r
from nextera_phagedisplayanalysis.abpred import meta as m
from nextera_utils.docker_interop import DockerInterop
import sys
import pandas as pd


def get_abpred_in_fn(in_fn):
    file_path = Path(in_fn)
    directory_path = file_path.parent
    out = os.path.join(directory_path, 'abpred_in.fasta')
    return out


def create_abpred_in_file(in_fn, abpred_in_fn):
    with open(in_fn, 'r') as file:
        content = file.read()
    in_fasta_content = ""
    lines_list = content.splitlines()
    for i in range(1, len(lines_list)):
        in_fasta_content += lines_list[i] + '\n'
    with open(abpred_in_fn, 'w') as f:
        f.write(in_fasta_content)


def run_abpred(pred_raw_in_fn, pred_tbl_out_fn, platform_map):
    abpred_in_fn = get_abpred_in_fn(pred_raw_in_fn)
    create_abpred_in_file(pred_raw_in_fn, abpred_in_fn)

    parser = ap.AbpredParser(ae.AbpredExecutor.get_out_dir(), platform_map)
    abpred_exec = ae.AbpredExecutor(abpred_in_fn, parser)
    abpred_exec.run(pred_tbl_out_fn)


print('Creating Developability-abpred report 2...')

# fn = "C:/docker_data_exchange/in/72c4309a-8f1c-43e4-8680-3dec807c5006/arguments.csv"
# docker = DockerInterop(fn, '72c4309a-8f1c-43e4-8680-3dec807c5006', '65051049-6583-449d-80b4-a76c7f3e9865')
docker = DockerInterop(sys.argv[1])

rank_type = docker.get_info_value(0, 'rank_type')
normalize_ranks = docker.get_info_value(0, 'normalize_ranks')
normalize_ranks = DockerInterop.parse_java_boolean(normalize_ranks)
round_ranks = docker.get_info_value(0, 'round_ranks')
round_ranks = DockerInterop.parse_java_boolean(round_ranks)

benchmark = b.Benchmark()

data_items = docker.get_data_items()

for item in data_items:
    in_fn = item[0]
    fig_out_fn = item[1]
    tbl_out_fn = item[2]
    tag = item[3]
    if tag=='prediction':
        pred_raw_in_fn = in_fn
        pred_tbl_out_fn = tbl_out_fn
    elif tag=='ranks':
        ranks_out_fn=tbl_out_fn
    elif tag=='meta':
        meta_out_fn = tbl_out_fn

platform_map = {}
platform_map['AS']='ACCSTAB'
platform_map['AC'] = 'ACSINS'
platform_map['BVP'] = 'BVPELISA'
platform_map['CSI'] = 'CSIBLI'
run_abpred(pred_raw_in_fn, pred_tbl_out_fn, platform_map)
ranks = r.Ranks(benchmark, platform_map, vs_original=True, rank_type=rank_type,
                normalize_ranks=normalize_ranks, round_ranks=round_ranks)
#print('rank:' + pred_tbl_out_fn)
#pred_tbl_out_fn= "C:/docker_data_exchange/out/65051049-6583-449d-80b4-a76c7f3e9865/Abpredtbl.csv"
df = pd.read_csv(pred_tbl_out_fn, sep='\t', index_col=False)
ranks_df = ranks.calculate(df)
#print('save:' + ranks_out_fn)
docker.write_csv(ranks_df, ranks_out_fn)

meta=m.Meta(ranks_df)
meta_df = meta.calculate()
docker.write_csv(meta_df, meta_out_fn)

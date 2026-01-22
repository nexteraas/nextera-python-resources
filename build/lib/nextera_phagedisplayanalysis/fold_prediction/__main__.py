import sys
from nextera_utils.docker_interop import DockerInterop


print('Creating fold prediction report...')


# fn = 'C:/docker_data_exchange/in/45a95f67-cc3d-4b46-bc8f-7c7d188a151d/arguments.csv'
# docker = DockerInterop(fn, '45a95f67-cc3d-4b46-bc8f-7c7d188a151d');
docker = DockerInterop(sys.argv[1])

predictor = docker.get_info_value(0, 'predictor')

data_items = docker.get_data_items()

if(predictor=='boltz1'):
    from nextera_phagedisplayanalysis.fold_prediction.boltz1_predictor import Boltz1Predictor
    print('Running Boltz1 prediction...')
    input_format = docker.get_info_value(0, 'boltz_input_format')
    accelerator = docker.get_info_value(0, 'boltz_accelerator')
    devices = docker.get_info_value(0, 'boltz_devices')
    output_format = docker.get_info_value(0, 'boltz_output_format')
    num_workers = docker.get_info_value(0, 'boltz_num_workers')
    pae = docker.get_info_value(0, 'boltz_pae')
    pae = (pae=='true')
    pde = docker.get_info_value(0, 'boltz_pde')
    pde = (pde == 'true')
    recycling_steps = docker.get_info_value(0, 'boltz_recycling_steps')
    sampling_steps = docker.get_info_value(0, 'boltz_sampling_steps')
    diffusion_samples  = docker.get_info_value(0, 'boltz_diffusion_samples')
    step_scale  = docker.get_info_value(0, 'boltz_step_scale')
    msa_pairing_strategy  = docker.get_info_value(0, 'boltz_msa_pairing_strategy')
    use_msa_server = docker.get_info_value(0, 'boltz_use_msa_server')
    use_msa_server = (use_msa_server == 'true')
    seed = docker.get_info_value(0, 'boltz_seed')
    if seed=='null':
        seed=None
    in_structure_fn = None
    out_structure_fn=None
    out_confidence_fn = None
    out_pae_fn = None
    out_pde_fn = None
    out_plddt_fn=None
    for item in data_items:
        in_fn = item[0]
        tag = item[3]
        fig_out_fn = item[1]
        tbl_out_fn = item[2]
        if tag=='structure':
            in_structure_fn = in_fn
            out_structure_fn = tbl_out_fn
        elif tag=='confidence':
            out_confidence_fn = tbl_out_fn
        elif tag == 'pae':
            out_pae_fn = fig_out_fn
        elif tag == 'pde':
            out_pde_fn = fig_out_fn
        elif tag == 'plddt':
            out_plddt_fn = fig_out_fn
    print('Input: ' + in_structure_fn)
    boltz = Boltz1Predictor(in_structure_fn, input_format=input_format, accelerator=accelerator, devices=devices,
                            output_format=output_format, num_workers=num_workers, pae=pae, pde=pde,
                            recycling_steps=recycling_steps, sampling_steps=sampling_steps,
                            diffusion_samples=diffusion_samples, step_scale=step_scale,
                            msa_pairing_strategy=msa_pairing_strategy, use_msa_server=use_msa_server, seed=seed)
    print('Output: ' + out_structure_fn)
    boltz.predict(out_structure_fn, out_confidence_fn, out_pae_fn, out_pde_fn, out_plddt_fn)
    print('Prediction done.')
elif (predictor=='igfold'):
    print('Running IgFold prediction...')
    from nextera_phagedisplayanalysis.fold_prediction.igfold_predictor import IgFoldPredictor
    igfold = IgFoldPredictor()
    for item in data_items:
        data_df = docker.read_csv(item[0])
        in_fn=item[1]
        out_fn=item[2]
        igfold.predict(data_df, out_fn)





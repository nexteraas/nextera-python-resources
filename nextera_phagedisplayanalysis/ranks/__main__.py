from nextera_utils.docker_interop import DockerInterop

print ('Ranks report:')

docker=DockerInterop();
print(docker.get_input_fn('testfn'))
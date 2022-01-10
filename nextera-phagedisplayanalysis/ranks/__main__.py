print ('Ranks report:')
from docker_interop import DockerInterop

docker=DockerInterop();
print(docker.get_input_fn('testfn'))
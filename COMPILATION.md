# Compilation details

## Compiling for Linux/PyPi on Windows using Docker

For the Windows terminal, I use Git Bash as readily available in
Git for Windows. Furthermore, make sure that Docker is installed.
Construct the build environment by building the Docker image
```
docker build . -t pymodia-pypi -f Dockerfile-linux-pypi
```

Modify the `build_docker_linux_pypi.sh` file and set the `ROOT` variable to the root
folder of this repository. Next, run the `docker_setup.sh` script

```
./build_docker_linux_pypi.sh
```

### Uploading to PyPi

This will place wheels in the `dist` folder. To upload these wheels
to PyPi, make sure you have `twine` installed using

```
pip install twine
```

To upload, run

```
python -m twine upload wheelhouse/*
```

## Compilation and testing under Linux Debian

Compile locally
```
python3 setup.py build
```

and install it locally
```
pip install -e .
```

and finally test it

```
pytest tests/*
```

from setuptools import Extension, setup
import os
import sys
import re

PKG = "pymodia"
VERSIONFILE = os.path.join(os.path.dirname(__file__), PKG, "_version.py")
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print(r"Unable to find version in %s" % (VERSIONFILE,))
        raise RuntimeError(r"If %s.py exists, it is required to be well-formed" % (VERSIONFILE,))

def find_windows_versions():
    """
    Autofind the msvc and winkit versions
    """
    root = os.path.join('C:', os.sep,'Program Files', 'Microsoft Visual Studio', '2022', 'Community', 'VC', 'Tools', 'MSVC')

    # for Gitlab actions, the above folder does not exist and this is communicated
    # back by providing None as the result
    if not os.path.exists(root):
        return None, None

    for file in os.listdir(root):
        if os.path.isdir(os.path.join(root, file)):
            msvcver = file
        
    root = os.path.join('C:', os.sep,'Program Files (x86)', 'Windows Kits', '10', 'Include')
    for file in os.listdir(root):
        if os.path.isdir(os.path.join(root, file)):
            winkitver = file

    return msvcver, winkitver

# specify paths on Windows to find compiler and libraries
if os.name == 'nt':
    msvc_ver, winkit_ver = find_windows_versions()

    if msvc_ver and winkit_ver:
        # only proceed with setting the paths for local development, i.e. when the
        # msvc_ver and winkit_ver variables are *not* None
        os.environ['PATH'] += r";C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\%s\bin\Hostx64\x64" % msvc_ver
        os.environ['PATH'] += r";C:\Program Files (x86)\Windows Kits\10\bin\%s\x64" % winkit_ver

        # set path to include folders
        os.environ['INCLUDE'] += r";C:\Program Files (x86)\Windows Kits\10\Include\%s\ucrt" % winkit_ver
        os.environ['INCLUDE'] += r";C:\Program Files (x86)\Windows Kits\10\Include\%s\shared" % winkit_ver
        os.environ['INCLUDE'] += r";C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\%s\include" % msvc_ver

        # some references to libraries
        os.environ['LIB'] += r";C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\%s\lib\x64" % msvc_ver
        os.environ['LIB'] += r";C:\Program Files (x86)\Windows Kits\10\Lib\%s\um\x64" % winkit_ver
        os.environ['LIB'] += r";C:\Program Files (x86)\Windows Kits\10\Lib\%s\ucrt\x64" % winkit_ver

        # also specify some custom paths for libraries
        os.environ['INCLUDE'] += r";C:\PROGRAMMING\LIBS\boost-1.74.0-win-x64\include"   # boost library
        os.environ['INCLUDE'] += r";D:\PROGRAMMING\LIBS\boost-1.74.0-win-x64\include"   # boost library
        os.environ['INCLUDE'] += r";C:\PROGRAMMING\LIBS\eigen-3.3.9"                    # eigen3 linear algebra library
        os.environ['INCLUDE'] += r";D:\PROGRAMMING\LIBS\eigen-3.3.9"                    # eigen3 linear algebra library
    else:
        # if msvc_ver and winkit_ver are set to None, this means we are working on Gitlab Actions
        # which requires the paths to be set differently; we here set the paths to eigen3 and boost
        os.environ['INCLUDE'] += r";" + os.environ['GITHUB_WORKSPACE'] + r"\vendor\eigen-3.4.0"
        os.environ['INCLUDE'] += r";" + os.environ['GITHUB_WORKSPACE'] + r"\vendor\boost_1_82_0"

        # re-order paths to ensure that the MSVC toolchain is in front; this needs to be done
        # because the Git bin folder precedes the MSVC bin folder, resulting in the wrong link.exe
        # executable to be used in the linking step
        paths = os.environ['PATH'].split(";")
        newpaths = []
        for path in paths:
            if "Microsoft Visual Studio" in path:
                newpaths = [path] + newpaths
            else:
                newpaths.append(path)
        os.environ['PATH'] = ";".join(newpaths)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pymodia',
    version=verstr,
    author="Joeri van Limpt",
    author_email="joerivanlimpt@hotmail.com",
    description="Python package making SVG images of molecular orbital diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ifilot/pymodia",
    ext_modules=cythonize(ext_modules[0],
                          language_level = "3",
                          build_dir="build"),
    packages=['pymodia'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    python_requires='>=3.5',
    install_requires=['numpy','drawvg'],
)

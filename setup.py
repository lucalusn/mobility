from setuptools import setup
import os
import re
import codecs
# Create new package with python setup.py sdist

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Create new package with python setup.py sdist
setup(
    name='PV simulator',
    version=find_version("pv_simulator", "__init__.py"),
    python_requires='>3.8.0',
    packages=['pv_simulator','runner'],
    url='',
    license='MIT',
    author='Lusnig Luca',
    install_requires=[                # since i am using basic function of numpy and pandas i do not pin theirs version
        "aio-pika == 6.8.0",
        "asyncio == 3.4.3",
        "numpy",
        "pandas"
    ],
    author_email='lusnig.luca@gmail.com',
    description='System that generates simulated photovoltaic power values in kW',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'run_meter.py = runner.run_meter:run_meter',
            'run_PV_simulator.py = runner.run_PV_simulator:run_PV'
        ]},
)

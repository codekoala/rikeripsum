from setuptools import setup
from glob import glob


DATA = list(glob('treksum/data/*.gzc'))


setup(
    name='treksum',
    version='1.2',
    packages=['treksum'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    data_files=[(
        'data', DATA
    )],
    package_data={
        '': ['*.gzc'] + [d.lstrip('treksum/') for d in DATA],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'treksum = treksum.treksum:main'
        ],
    }
)

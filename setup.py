from distutils.core import setup

setup(
    name='treksum',
    version='1.2',
    packages=['treksum'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    data_files=[(
        'data', [
            'treksum/data/riker.gzc'
        ]
    )],
    package_data={
        '': ['*.gzc', 'data/riker.gzc'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts':
        ['treksum=treksum:main'],
    }
)

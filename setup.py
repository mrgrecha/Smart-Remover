from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='Smart_RM',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    
     entry_points={
        'console_scripts':
            [
            'trash = source.bin:main',
            'srm = source.remove:main',
            'config = source.config_maker:main',
            'undo = source.undo:main'
            ]
        },
       include_package_data=True
)
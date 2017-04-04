from setuptools import setup, find_packages
from os.path import join, dirname
import source

setup(
    name='Smart_RM',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    
     entry_points={
        'console_scripts':
            [
            'smart = source.main:main',
            'bin = source.bin:main',
            'srm = source.remove:main',
            'rec = source.recover:main'
            ]
        },
       include_package_data=True
)
from setuptools import find_packages
from setuptools import setup


setup(
    name='pre_commit_hooks_dvolgyes',
    description='Some out-of-the-box hooks for pre-commit.',
    url='https://github.com/dvolgyes/pre-commit-hooks',
    version='0.1.0',

    author='David Volgyes',
    author_email='david.volgyes@ieee.org',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        # quickfix to prevent pycodestyle conflicts
        'flake8!=2.5.3',
        'autopep8>=1.3',
        'pyyaml',
        'six',
#        'python-magic',
    ],
    entry_points={
        'console_scripts': [
            'detect-dicom = pre_commit_hooks.detect_dicom:detect_dicom',
        ],
    },
)

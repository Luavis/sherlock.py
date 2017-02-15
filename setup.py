#!/usr/bin/env python
import sherlock
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

def install():

    setup(
        name='sherlock.py',
        version=sherlock.__version__,
        description='Python to shell script transcompiler',
        long_description=readme,
        author=sherlock.__author__,
        author_email=sherlock.__email__,
        license='MIT',
        platforms=['POSIX'],
        url='https://github.com/Luavis/sherlock',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: MIT License',
            'Environment :: Console',
            'Operating System :: POSIX',
            'Operating System :: MacOS :: MacOS X',
            'Topic :: Software Development :: Compilers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',],
        packages=find_packages(exclude=('tests', 'samples', )),
        entry_points={'console_scripts': [
            'sherlock = sherlock:execute_from_command_line',
        ]},
        install_requires=[
            'pytest==3.0.5',
        ],
    )

if __name__ == "__main__":
    install()

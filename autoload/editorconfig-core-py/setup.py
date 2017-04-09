from setuptools import setup
import editorconfig

setup(
    name='EditorConfig',
    version=editorconfig.__version__,
    author='EditorConfig Team',
    packages=['editorconfig'],
    url='http://editorconfig.org/',
    license='LICENSE.txt',
    description='EditorConfig File Locator and Interpreter for Python',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'editorconfig = editorconfig.main:main',
        ]
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)

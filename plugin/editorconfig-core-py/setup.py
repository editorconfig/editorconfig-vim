from setuptools import setup
import editorconfig

setup(
    name='EditorConfig',
    version=editorconfig.__version__,
    author='EditorConfig Team',
    packages=['editorconfig'],
    namespace_packages=['editorconfig'],
    url='http://editorconfig.org/',
    license='LICENSE.txt',
    description='EditorConfig File Locator and Interpreter for Python',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'editorconfig.py = editorconfig.main:main',
        ]
    },
)

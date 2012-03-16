from setuptools import setup

setup(
    name='EditorConfig',
    version='0.9.0-alpha',
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
)

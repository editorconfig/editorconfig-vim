from setuptools import setup

setup(
    name='EditorConfig',
    version='0.9.0-alpha',
    author='EditorConfig Team',
    packages=['editorconfig'],
    url='http://editorconfig.org/',
    entry_points = {
        'console_scripts': [
            'editorconfig = editorconfig.main:main',
        ]
    },
)

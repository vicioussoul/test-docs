from setuptools import setup, find_packages

setup(
    name='internal_docs',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'sphinx.html_themes': [
            'sphinx_internal_search = sphinx_internal_search',
        ]
    },
)
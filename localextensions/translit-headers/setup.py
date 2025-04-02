from setuptools import setup, find_packages

setup(
    name="translit-headers",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Unidecode',
    ],
    description="Sphinx extension for header transliteration",
    author="DevOps TW",
    author_email="mymail@mail.mail",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Documentation",
        "Framework :: Sphinx :: Extension",
    ],
)
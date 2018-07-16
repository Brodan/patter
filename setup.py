import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md'), encoding='utf8').read()
except IOError:
    README = ''

setup(
    name="patter",
    version="0.1.0",
    author="Christopher Hranj",
    author_email="christopher.hranj@gmail.com",
    description="Pipe stdout directly to Mattermost channels or users.",
    long_description=README,
    long_description_content_type='text/markdown',
    license="MIT",
    keywords="patter mattermost",
    url="https://github.com/brodan/patter",
    install_requires=[
        "mattermostdriver>=5.0.0",
    ],
    packages=find_packages(),
    include_package_data=True,
    scripts=[
        "bin/patter",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities",
    ],
)

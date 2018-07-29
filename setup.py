from os import path
from setuptools import setup, find_packages


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    README = f.read()

setup(
    name="patter",
    version="0.2.1",
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

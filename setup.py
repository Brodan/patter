from setuptools import setup, find_packages


setup(
    name="patter",
    version="0.1.0",
    author="Christopher Hranj",
    author_email="christopher.hranj@gmail.com",
    description="Pipe stdout directly to Mattermost channels or users.",
    license="MIT",
    keywords="patter mattermost",
    url="https://github.com/brodan/patter",
    install_requires=[
        "mattermostdriver==5.0.0",
    ],
    packages=find_packages(),
    include_package_data=True,
    scripts=[
        "bin/patter",
    ],
)

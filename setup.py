from os import path

from setuptools import setup

with open("mapID_to_collection_DB/version.py") as f:
    exec(f.read())


def get_long_description() -> str:
    fname = path.join(path.dirname(path.abspath(__file__)), "README.rst")
    with open(fname, "r") as f:
        return f.read()


setup(
    name="mapID_to_collection_DB",
    description="",
    long_description=get_long_description(),
    author="Kuuuube",
    author_email="",
    license="GPL-3.0 License",
    url="",
    download_url="",
    install_requires=[
        "requests~=2.26.0"
    ],
    python_requires=">=3.10",
    project_urls={
        "Issue Tracker": "https://github.com/Kuuuube/osu_MapID_to_Collection_DB/issues",
        "Source": "https://github.com/Kuuuube/osu_MapID_to_Collection_DB",
    },
    version=VERSION,
)
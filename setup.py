import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "osu_collection_factory", "__version__.py"), "r") as v:
    exec(v.read(), about)


def get_long_description() -> str:
    fname = os.path.join(here, "README.md")

    with open(fname, "r") as f:
        return f.read()


setup(
    name=about["__title__"],
    description=about["__description__"],
    long_description=get_long_description(),
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    url=about["__url__"],
    download_url="",
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    python_requires=">=3.10",
    project_urls={
        "Issue Tracker": "https://github.com/Kuuuube/osu_collection_factory/issues",
        "Source": "https://github.com/Kuuuube/osu_collection_factory",
    },
    version=about["__version__"],
)

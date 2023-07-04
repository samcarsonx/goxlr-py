from setuptools import setup, find_packages
from version import __version__

setup(
    name="goxlr",
    version=__version__,
    description="A Python wrapper for the GoXLR Utility API.",
    url="https://github.com/samcarsonx/goxlr",
    author="Sam Carson",
    author_email="sam@samcarson.co.uk",
    license="MIT",
    packages=find_packages(),
    install_requires=["asyncio", "websockets"],
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

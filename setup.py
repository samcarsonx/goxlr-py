from setuptools import setup, find_packages

# Thanks to https://stackoverflow.com/a/7071358
import re

VERSIONFILE = "goxlr/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="goxlr",
    version=verstr,
    description="A Python wrapper for the GoXLR Utility API.",
    url="https://github.com/samcarsonx/goxlr-py",
    author="Sam Carson",
    author_email="sam@samcarson.co.uk",
    license="MIT",
    packages=find_packages(),
    install_requires=["asyncio", "websockets"],
    python_requires=">=3.10",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

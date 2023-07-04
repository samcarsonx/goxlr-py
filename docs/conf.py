import os
import sys

# Add your project directory to the Python path
sys.path.insert(0, os.path.abspath(".."))

from ..version import __version__

# Project information
project = "goxlr"
author = "Sam Carson"
version = __version__
release = __version__

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

# Autodoc configuration
autodoc_member_order = "alphabetical"

# HTML theme
html_theme = "sphinx_rtd_theme"

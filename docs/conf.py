import os
import sys

# Add your project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Project information
project = "goxlr"
author = "Sam Carson"

from version import __version__

version = __version__
release = __version__

# Extensions
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser"]

# Autodoc configuration
autodoc_member_order = "alphabetical"

# HTML theme
html_theme = "sphinx_rtd_theme"

source_suffix = [".rst", ".md"]

master_doc = "index"

import datetime
import os
import sys

# Add your project root directory to the Python path
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "goxlr"
author = "Sam Carson"
# Get year
copyright = f"{datetime.datetime.now().year}, {author}"

from goxlr import __version__

version = __version__
release = __version__

# Extensions
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_mdinclude"]

# Autodoc configuration
autodoc_member_order = "bysource"

# HTML theme
html_theme = "sphinx_rtd_theme"

master_doc = "index"

# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
project = 'first_cycling_api'
copyright = '2021, Ethan Baron'
author = 'Ethan Baron'
release = '0.1.0' # The full version, including alpha/beta/rc tags


# -- General configuration ---------------------------------------------------
import sphinx_rtd_theme
extensions = ['sphinx.ext.napoleon', 'sphinx.ext.autodoc', "sphinx_rtd_theme"]

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

autodoc_member_order = 'bysource' # So autodoc lists members in the order found in the source code, rather than alphabetically
autodoc_default_options = {'inherited-members': True, 'members': None}
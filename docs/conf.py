# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sphinx_rtd_theme

from os import path, environ
import sys
sys.path.insert(0, path.abspath('../src'))
from ghrs import __version__

# -- Project information -----------------------------------------------------

project = 'GHRS'
copyright = '2021, Data and Smart Technologies.'
author = 'Data and Smart Technologies'

# The full version, including alpha/beta/rc tags
release = __version__
version = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx_rtd_theme', 'sphinx.ext.napoleon', 'sphinx_copybutton'
]

# The master toctree document.
master_doc = 'index'

intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
'pandas': ('https://pandas.pydata.org/docs/', None),
'openpyxl': ('https://openpyxl.readthedocs.io/en/stable', None),
'numpy': ('https://numpy.org/doc/stable', None),
'requests': ('https://docs.python-requests.org/en/master/', None)
}

autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': False,
    'exclude-members': '__weakref__',
    'autoclass_content': 'class',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '*.migrations.rst', 'manage.rst']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = 'GHRS'

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = ' '

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

html_show_sourcelink = False
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = './_static/icons/xsight-light.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = './_static/icons/favicon.ico'
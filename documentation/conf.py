# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 
              'sphinx_design', 
              'sphinxcontrib.images', 
              'sphinx_copybutton', 
              'example_plate',
              'internal_docs',]
myst_enable_extensions = {
    'colon_fence',
    'tasklist',
    'attrs_block',
    'attrs_inline',
    'linkify',
    'fieldlist',      
}

language = 'ru'

exclude_patterns = ['_includes/*']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
templates_path = ['_templates']
html_show_sphinx = 0
html_favicon = '_static/favicon.ico'
html_logo = '_static/logo-prod.png'
html_css_files = ['css/custom.css', 'css/example_plate.css']

html_theme_options = {
    "home_page_in_toc": True,
    "toc_title": " На этой странице:",
    "article_header_start": "breadcrumbs", # хлебные крошки в хедере
    "article_header_end": "button-1",
    "max_navbar_depth": 3, # регулирует глубину содержания в левом навбаре
    "show_toc_level": 4, # регулирует глубину содержания в правом навбаре
}

def setup(app):
    app.add_js_file("js/tooltip.js")

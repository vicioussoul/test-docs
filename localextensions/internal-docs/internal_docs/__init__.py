from sphinx.application import Sphinx
from .search import setup_internal_search

def setup(app: Sphinx):
    app.add_config_value('internal_search_path', 'internal/*', 'html')
    app.add_config_value('internal_search_page', 'internal/main', 'html')
    app.connect('html-page-context', setup_internal_search)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
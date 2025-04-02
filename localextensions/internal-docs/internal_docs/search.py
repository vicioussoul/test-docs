import json
from pathlib import Path
from sphinx.util import logging

logger = logging.getLogger(__name__)

def setup_internal_search(app, pagename, templatename, context, doctree):
    # Генерируем кастомный индекс для internal/*
    if app.builder.name == 'html':
        searchindex_path = Path(app.outdir) / 'searchindex.js'
        if searchindex_path.exists():
            with open(searchindex_path, 'r', encoding='utf-8') as f:
                data = f.read().replace('Search.setIndex(', '').replace(')', '')
                index = json.loads(data)

            # Создаём индекс только для internal/*
            internal_index = {
                'docnames': [name for name in index['docnames'] if name.startswith('internal/')],
                'titles': [],
                'filenames': [],
                'terms': {},
                'titleterms': {}
            }

            for i, name in enumerate(index['docnames']):
                if name.startswith('internal/'):
                    internal_index['titles'].append(index['titles'][i])
                    internal_index['filenames'].append(index['filenames'][i])

            for term, docs in index['terms'].items():
                filtered_docs = [doc_id for doc_id in docs if index['docnames'][doc_id].startswith('internal/')]
                if filtered_docs:
                    internal_index['terms'][term] = filtered_docs

            for term, docs in index['titleterms'].items():
                filtered_docs = [doc_id for doc_id in docs if index['docnames'][doc_id].startswith('internal/')]
                if filtered_docs:
                    internal_index['titleterms'][term] = filtered_docs

            # Сохраняем новый индекс
            internal_index_path = Path(app.outdir) / '_searchindex_internal.json'
            with open(internal_index_path, 'w', encoding='utf-8') as f:
                json.dump(internal_index, f)
            logger.info(f"Generated internal search index at {internal_index_path}")

    # Модифицируем основной поиск, чтобы исключить internal/*
    context['script_files'].append('_static/custom_search.js')  # Добавляем кастомный JS

    # Добавляем второй поиск на указанную страницу
    if pagename == app.config.internal_search_page:
        context['script_files'].append('_searchindex_internal.json')
        context['extra_html'] = """
        <div>
            <h2>Internal Search</h2>
            <input type="text" id="internal-searchbox" placeholder="Search in /internal/* only">
            <div id="internal-searchresults"></div>
        </div>
        <script type="text/javascript">
            function initInternalSearch() {
                var internalSearch = new Searcher();
                internalSearch.loadIndex('/_searchindex_internal.json');
                document.getElementById('internal-searchbox').addEventListener('input', function(e) {
                    internalSearch.search(e.target.value, function(results) {
                        var resultDiv = document.getElementById('internal-searchresults');
                        resultDiv.innerHTML = '';
                        results.forEach(function(result) {
                            resultDiv.innerHTML += '<p><a href="' + result.docname + '.html">' + result.title + '</a></p>';
                        });
                    });
                });
            }
            document.addEventListener('DOMContentLoaded', initInternalSearch);
        </script>
        """

def create_custom_search_js(app):
    # Создаём кастомный JS для фильтрации основного поиска
    custom_js = """
    document.addEventListener('DOMContentLoaded', function() {
        var originalSearch = Search.performSearch;
        Search.performSearch = function(query) {
            originalSearch.call(this, query);
            var results = this._results.filter(function(result) {
                return !result.docname.startsWith('internal/');
            });
            this._results = results;
            this.displayResults();
        };
    });
    """
    custom_js_path = Path(app.outdir) / '_static' / 'custom_search.js'
    custom_js_path.parent.mkdir(exist_ok=True)
    with open(custom_js_path, 'w', encoding='utf-8') as f:
        f.write(custom_js)
    logger.info(f"Generated custom search JS at {custom_js_path}")

# Подключаем создание кастомного JS
def setup(app):
    app.connect('html-page-context', setup_internal_search)
    app.connect('builder-inited', create_custom_search_js)
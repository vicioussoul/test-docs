import re
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

def source_read_handler(app: Sphinx, docname: str, source: list):
    text = source[0]
    lines = text.splitlines()
    
    # Получаем URI для текущего документа, например "subdir/doc.html"
    target_uri = app.builder.get_target_uri(docname)
    if not target_uri.startswith('/'):
        target_uri = '/' + target_uri

    # Регулярные выражения для строк :link: и :link-type:
    pattern_link = re.compile(r"^(\s*:link:\s*)(#[^\s]+)")
    pattern_link_type = re.compile(r"^(\s*:link-type:\s*)\S+")

    # Проходим по всем строкам исходного текста
    for i, line in enumerate(lines):
        m_link = pattern_link.match(line)
        if m_link:
            # Если нашли строку с :link:, значение которой начинается с '#'
            # ищем в соседних строках (до 2-х строк вверх и вниз) наличие :link-type:
            update_needed = False
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                if j != i and pattern_link_type.match(lines[j]):
                    # Если нашли :link-type: рядом – меняем его значение на url
                    lines[j] = pattern_link_type.sub(r"\1url", lines[j])
                    update_needed = True
            if update_needed:
                # Обновляем строку :link: — подставляем перед якорем URI текущего документа.
                anchor = m_link.group(2)  # например, "#section"
                new_link = target_uri + anchor  # например, "/subdir/doc.html#section"
                lines[i] = m_link.group(1) + new_link
                logger.info("In doc '%s': updated :link: %s -> %s", docname, anchor, new_link)

    source[0] = "\n".join(lines)

def setup(app: Sphinx):
    app.connect("source-read", source_read_handler)
    logger.info("Extension loaded: If :link: and :link-type: are within 2 lines, :link-type: is forced to 'url'")
    return {"version": "0.1", "parallel_read_safe": True}
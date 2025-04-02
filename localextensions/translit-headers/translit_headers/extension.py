import unidecode
from docutils import nodes
from docutils.transforms import Transform
from sphinx.util import logging

logger = logging.getLogger(__name__)

def update_ids_in_tree(tree):
    slug_counts = {}
    for section in tree.traverse(nodes.section):
        title_node = section.next_node(nodes.title)
        if not title_node:
            continue
        title_text = title_node.astext()
        base_slug = unidecode.unidecode(title_text).lower().replace(' ', '-')
        count = slug_counts.get(base_slug, 0)
        new_id = base_slug if count == 0 else f"{base_slug}-{count}"
        slug_counts[base_slug] = count + 1
        section['ids'] = [new_id]
        section['names'] = [new_id]
        logger.info("Updated section '%s' to id '%s'", title_text, new_id)

class TransliterateIDsTransform(Transform):
    default_priority = 500
    def apply(self):
        update_ids_in_tree(self.document)
        
def setup(app):
    app.add_transform(TransliterateIDsTransform)
    logger.info("translit-headers extension loaded (using Transform)")
    return {'version': '0.1', 'parallel_read_safe': True}
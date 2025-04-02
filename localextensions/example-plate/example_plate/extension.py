# This extension adds a custom admonition for examples in text

from docutils import nodes
from docutils.parsers.rst import Directive, directives

class ExampleAdmonition(Directive):
    required_arguments = 0  # Заголовок не обязателен
    optional_arguments = 1  # Можно передать заголовок как аргумент
    final_argument_whitespace = True
    option_spec = {
        'title': directives.unchanged,  # Позволяет задать заголовок через опцию :title:
    }
    has_content = True

    def run(self):
        admonition_node = nodes.admonition()

        # Определяем текст заголовка:
        # Приоритет: опция > аргумент > значение по умолчанию
        title_text = self.options.get('title')
        if not title_text and self.arguments:
            title_text = self.arguments[0]
        if not title_text:
            title_text = "Пример"

        # Создаем узел заголовка и добавляем его в admonition
        title_node = nodes.title(title_text, title_text)
        admonition_node += title_node

        # Обрабатываем содержимое директивы
        self.state.nested_parse(self.content, self.content_offset, admonition_node)
        return [admonition_node]
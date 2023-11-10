from django import template
import re

register = template.Library()

@register.filter
def format_text(value):
    link_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def replace_link(match):
        url = match.group()
        return f'<a href="{url}">{url}</a>'

    # Заменяем найденные ссылки на HTML-теги
    formatted_text = re.sub(link_pattern, replace_link, value)
    return formatted_text
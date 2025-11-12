from django import template

register = template.Library()


@register.filter(name='lookup')
def lookup(dictionary, key):
    """
    Template filter to lookup a dictionary value by key.
    Usage in template: {{ dict|lookup:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key, '')


@register.filter(name='get_field_label')
def get_field_label(field_categories, field_name):
    """
    Get the human-readable label for a field name from field categories.
    Usage in template: {{ field_categories|get_field_label:field_name }}
    """
    for category, fields in field_categories.items():
        if field_name in fields:
            return fields[field_name]
    return field_name.replace('_', ' ').title()

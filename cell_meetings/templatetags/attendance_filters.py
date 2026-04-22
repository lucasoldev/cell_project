from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Returns the dictionary value to the key"""
    if dictionary is None:
        return False
    return dictionary.get(key, False)

@register.filter
def count_true(dictionary):
    """Count how many True values are in the dictionary"""
    if not dictionary:
        return 0
    return sum(1 for v in dictionary.values() if v)

@register.filter
def month_name(month_num):
    """Return the month name in portugues"""
    months = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março',
        4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro',
        10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    try:
        return months.get(int(month_num), '')
    except (ValueError, TypeError):
        return ''

@register.filter
def percentage(value, total):
    """Calculate the percentage"""
    # ✅ Converte para int se for QuerySet
    if hasattr(total, 'count'):
        total = total.count()
    try:
        total = int(total)
        value = int(value)
    except (ValueError, TypeError):
        return 0
    
    if total == 0:
        return 0
    return round((value / total) * 100, 1)

@register.filter
def split(value, separator):
    """Split a string"""
    return value.split(separator)

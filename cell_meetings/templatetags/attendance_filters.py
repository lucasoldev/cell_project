from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Retorna o valor do dicionário para a chave"""
    if dictionary is None:
        return False
    return dictionary.get(key, False)


@register.filter
def count_true(dictionary):
    """Conta quantos valores True existem no dicionário"""
    if not dictionary:
        return 0
    return sum(1 for v in dictionary.values() if v)


@register.filter
def percentage(value, total):
    """Calcula porcentagem"""
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
    """Divide uma string"""
    return value.split(separator)

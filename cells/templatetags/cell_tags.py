from django import template

register = template.Library()


@register.filter
def cell_display(cell):
    """
    Returns only the cell name for RED area (MAG).
    For other areas, returns "Cell Name - Area Color".
    """
    if not cell:
        return ""
    
    if cell.area.color == 'RED':
        return cell.name
    return f"{cell.name} - {cell.area.get_color_display()}"

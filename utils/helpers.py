# frontend/utils/helpers.py
import math

PAGE_SIZE = 6  # Número de productos por página

def paginate_list(items, page_num, page_size=PAGE_SIZE):
    """
    Divide una lista en páginas.
    Retorna (items_de_la_página, total_de_páginas).
    """
    total = len(items)
    start = (page_num - 1) * page_size
    end = start + page_size
    return items[start:end], math.ceil(total / page_size) if total > 0 else 1

def currency_fmt(amount, currency="COP"):
    """
    Formatea un número como precio con separadores de miles.
    """
    try:
        return f"{amount:,.0f} {currency}"
    except Exception:
        return f"{amount} {currency}"

from django import template

register = template.Library()

@register.filter(name='spacecomma')
def spacecomma(value):
    s_text = ''
    money = str(value)[::-1]
    for i in range(len(money)//3+1):
        s_text+=money[3*i:3*i+3]+' '
    return s_text.strip()[::-1]

@register.filter(name='real_money')
def real_money(price, percentage):
    return spacecomma((price*(100+percentage))//100)
    # s_text = ''
    # money = str(value)[::-1]
    # for i in range(len(money)//3+1):
    #     s_text+=money[3*i:3*i+3]+' '
    # return s_text.strip()[::-1]

@register.filter(name='bool_to_word')
def bool_to_word(value):
    if value: return "Ha"
    return "Yo'q"

@register.filter(name='subtract')
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return ""

@register.filter(name='break_func')
def break_func(value, chunk_size=25):
    ans = ''
    for i in range(0, len(value), chunk_size):
        ans += value[i:i + chunk_size] + ''
    return ans

@register.filter(name='define_cur_month')
def define_cur_month(value):
    value = int(value)
    months_table = {
        1:'Yanvar',
        2:'Fevral',
        3:'Mart',
        4:'Aprel',
        5:'May',
        6:'Iyun',
        7:'Iyul',
        8:'Avgust',
        9:'Sentyabr',
        10:'Oktabr',
        11:'Noyabr',
        0:'Dekabr',

    }
    return months_table[value%12]

@register.filter(name='define_cur_year')
def define_cur_year(value):
    value = int(value)
    return value//12
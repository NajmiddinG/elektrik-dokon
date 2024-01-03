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


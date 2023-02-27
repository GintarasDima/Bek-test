# Для реализации перечисленных требований необходимо определить модель данных,
# в которой будут храниться данные для вывода меню. Модель должна включать
# поля id, name (название пункта меню), parent (родительский пункт),
# order (порядок пункта в родительском пункте), url (url пункта меню).

# Далее необходимо реализовать шаблон tag, который будет принимать на вход название меню
# и на основании запроса к БД возвращать HTML код древовидного меню с учетом данных из модели.
# В качестве фреймворка для отрисовки используется Bootstrap.

# В админке Django необходимо добавить специальный интерфейс для управления меню.
# Этот интерфейс должен позволять создавать, редактировать и удалять пункты меню.

# Для определения активного пункта меню необходимо использовать механизм URL routing.
# Для этого необходимо добавить дополнительное поле в модель данных - is_active.
# В шаблон тэга добавляется код, который берет текущий URL и сравнивает его с URL
# пунктов меню из модели, а затем устанавливает значение is_active в true для пункта меню,
# соответствующего текущему URL.



#1) Создать модель для данных меню.Например:

class MenuItem(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField()


#2) Добавить модель в админку Django:

from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'parent')


#3) Создать тег для отображения меню:

from django import template
from .models import MenuItem

register = template.Library()



@ register.simple_tag
def show_menu(name):
    menu_items = MenuItem.objects.filter(parent__isnull=True).order_by('order')
    html = '<ul>'
    for item in menu_items:
        html += f'<li><a href="{item.url}">{item.name}</a>'
        # Вывод первого уровня вложенности
        submenu_items = MenuItem.objects.filter(parent=item).order_by('order')
        if submenu_items:
            html += '<ul>'
            for subitem in submenu_items:
                html += f'<li><a href="{subitem.url}">{subitem.name}</a></li>'
            html += '</ul>'
        html += '</li>'
    html += '</ul>'
    return html

# 4) Добавить тег в шаблон:

# < !DOCTYPE html >
# < html >
#   < head >
#     < title > MyPage < / title >
#   < / head >
#   < body >
#     { % show_menu 'main_menu' %}
#   < / body >
# < / html >



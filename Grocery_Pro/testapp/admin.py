from django.contrib import admin
from testapp.models import Grocery_Item_Model

class Grocery_Admin(admin.ModelAdmin):
    list_display = ['item_name', 'item_status', 'item_quantity', 'date']


admin.site.register(Grocery_Item_Model, Grocery_Admin)
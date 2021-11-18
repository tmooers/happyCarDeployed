# Register your models here.
from django.contrib import admin

from .models import Customer, PartType, Part, Cart, Order, NewsLetterUsers

admin.site.register(Customer)
admin.site.register(PartType)
admin.site.register(Part)
admin.site.register(Cart)
admin.site.register(Order)

class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email','date_added')

admin.site.register(NewsLetterUsers, NewsLetterAdmin)
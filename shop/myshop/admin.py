from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product
from .models import ContactMessage
from .models import Subscription


admin.site.register(Subscription)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    search_fields = ['name', 'email', 'subject']
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_1_show', 'image_2_show', 'image_3_show', 'price', 'available', 'created',
                    'uploaded']
    list_filter = ['available', 'created', 'uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}

    def image_1_show(self, obj):
        if obj.image_1:
            return mark_safe("<img src='{}' width='60' />".format(obj.image_1.url))
        return "None"

    def image_2_show(self, obj):
        if obj.image_2:
            return mark_safe("<img src='{}' width='60' />".format(obj.image_2.url))
        return "None"

    def image_3_show(self, obj):
        if obj.image_3:
            return mark_safe("<img src='{}' width='60' />".format(obj.image_3.url))
        return "None"

    image_1_show.short_description = "Картинка 1"
    image_2_show.short_description = "Картинка 2"
    image_3_show.short_description = "Картинка 3"

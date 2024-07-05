from django.contrib import admin
from cal.models import ItemType, MaterialGroup, CreateCode, ColorCode

# Register your models here.

class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_additive')

class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ('id','item_name', 'value', 'material_group', 'product_hierarchy_a','product_hierarchy_b','item_type_choice')
    list_filter = ('item_type_choice',)

class CreateCodedmin(admin.ModelAdmin):
    list_display = ('id', 'additive', 'liquied_narrow', 'swu', 'additive_type','resin','special_attribute')

class ColorCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'color_code', 'material_group', 'color_type_choice')

# Register your models here.
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(MaterialGroup, MaterialGroupAdmin)
admin.site.register(CreateCode, CreateCodedmin)
admin.site.register(ColorCode, ColorCodeAdmin)
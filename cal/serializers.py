from rest_framework import serializers
from .models import MaterialGroup, ColorCode




class ColorCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorCode
        fields = ['id','color_code', 'material_group', 'color_type_choice']


class MaterialGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialGroup
        fields = ['id', 'item_name', 'value', 'material_group', 'product_hierarchy_a', 'product_hierarchy_b']
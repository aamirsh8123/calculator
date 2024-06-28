from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ItemType(models.Model):
    name = models.CharField(max_length=100)
    is_additive = models.BooleanField(default=False, verbose_name="Is it additive?")
    def __str__(self):
        return self.name
    
class MaterialGroup(models.Model):
    item_name = models.CharField(max_length=200, null=False, blank=False)
    value = models.CharField(max_length=50,null=True, blank=True)
    material_group = models.CharField(max_length=100, null=True, blank=True)
    product_hierarchy_a = models.CharField(max_length=100, null=True, blank=True)
    product_hierarchy_b = models.CharField(max_length=100, null=True, blank=True)
    item_type_choice = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.item_name
    
class ColorCode(models.Model):
    color_code = models.CharField(
        max_length=100,
        verbose_name=_('Color Code')
        )
    material_group = models.CharField(
        max_length=100,
        verbose_name=_('Color Code Value'),
        null=False,
        blank=False,
        )
    color_type_choice = models.ForeignKey(
        MaterialGroup, 
        on_delete=models.SET_NULL,
        verbose_name=_('Color'),
        null=True, 
        blank=True
        )

    def __str__(self):
        return self.color_code

class CreateCode(models.Model):
    additive = models.CharField(max_length=100, null=False, blank=False,verbose_name='Is it Additive?:')
    liquied_narrow = models.ForeignKey(
        MaterialGroup, 
        on_delete=models.CASCADE,
        verbose_name=_("Is it for Liquid Packaging or a Narrow Web?:"), 
        null=True, 
        blank=True, 
        related_name='liquied_narrow'
        )
    swu = models.ForeignKey(MaterialGroup, verbose_name=_("Is it Solven, Water, UV?:"), on_delete=models.CASCADE, related_name='swu',null=False, blank=False, )

    additive_type = models.ForeignKey(
        MaterialGroup,
        verbose_name=_("What Additive Type or Industry Served?:"),
        on_delete=models.CASCADE,
        related_name='additive_type', 
        null=False, 
        blank=False
        )
    resin = models.ForeignKey(
        MaterialGroup,
        verbose_name=_("What Resin is mostly Used?:"),
        on_delete=models.CASCADE,
        related_name='resin', 
        null=True, 
        blank=True,
        )
    special_attribute = models.ForeignKey(
        MaterialGroup, 
        verbose_name=_("Any Special Attributes (Fade Resist, Fluorescents, Low Copper):"),
        on_delete=models.CASCADE,
        related_name='special_attribute',
        null=True, 
        blank=True
        )
    special_requirement = models.ForeignKey(
        MaterialGroup,
        verbose_name=_("What Type of Special Requirements:"),
        on_delete=models.CASCADE,
        related_name='special_requirement', 
        null=True, 
        blank=True
        )
    ink_type = models.ForeignKey(
        MaterialGroup, 
        verbose_name=_("Ink Type:"),
        on_delete=models.CASCADE,
        related_name='ink_type',
        null=True, 
        blank=True
        )
    color_type = models.ForeignKey(
        MaterialGroup, 
        verbose_name=_("Color:"),
        on_delete=models.CASCADE,
        related_name='color_type',
        null=True, 
        blank=True
        )
    color_code_choice = models.ForeignKey(
        ColorCode,
        verbose_name=_('Color Code:'),
        on_delete=models.SET_NULL,
        related_name='color_code_choice',
        null=True,
        blank=True,
    )
    press = models.ForeignKey(
        MaterialGroup,
        verbose_name=_("Press:"),
        on_delete=models.CASCADE,
        related_name='press',
        null=True, 
        blank=True
        )
    mg_code = models.CharField(
        max_length=200, 
        null=False, 
        blank=False,
        verbose_name=_("Material Group Code:"),
        )
    ph_code = models.CharField(
        max_length=200, 
        null=False, 
        blank=False,
        verbose_name=_("Product Hierarchy Code:"),
        )

    def __str__(self):
        return self.additive

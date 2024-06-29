from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from cal.models import MaterialGroup, CreateCode, ColorCode
from crispy_forms.layout import Layout, Fieldset, Div, Row, Column, Reset
from crispy_forms.bootstrap import FormActions
from django.utils.translation import gettext_lazy as _


class MaterialGroupForm(forms.ModelForm):
    class Meta:
        model = MaterialGroup
        fields = ['item_name', 'value', 'material_group', 'product_hierarchy_a', 'product_hierarchy_b', 'item_type_choice']

    def __init__(self, *args, **kwargs):
        super(MaterialGroupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div('item_name', css_class='col-md-6 mt-4'), 
                    Div('material_group', css_class='col-md-6 mt-4'),
                    css_class='row'   
                ),
                Div(
                    css_class='row' 
                ),
                Div(
                    Div('product_hierarchy_a', css_class='col-md-6'),
                    Div('product_hierarchy_b', css_class='col-md-6'),
                    css_class='row' 
                ),
                Div(
                    Div('item_type_choice', css_class='col-md-6'),
                    css_class='row' 
                ),
            ),
            FormActions(
                Submit('submit', 'Submit'),
            ),
        )

class ColorCodeForm(forms.ModelForm):
    color_type_choice = forms.ModelChoiceField(
        queryset=MaterialGroup.objects.filter(item_type_choice=13),
        label='Color'
    )
    class Meta:
        model = ColorCode
        fields = ['color_code', 'material_group', 'color_type_choice']
    
    def __init__(self, *args, **kwargs):
        super(ColorCodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div('color_code', css_class='col-md-6 mt-4'),
                    Div('material_group', css_class='col-md-6 mt-4'),
                    Div('color_type_choice', css_class='col-md-6 mt-4'),
                    css_class='row'   
                ),
            FormActions(
                Submit('submit', 'Save'),
            ),
            )
        )


class CodeCalculator(forms.ModelForm):
    additive = forms.ModelChoiceField(
        queryset = MaterialGroup.objects.filter(item_type_choice=1),
        label='Is it Additive?',
    )
    class Meta:
        model = CreateCode
        fields = ['additive','liquied_narrow','swu','additive_type','resin', 'special_attribute','special_requirement','ink_type','color_type', 'color_code_choice', 'press','mg_code','ph_code']
        
    def __init__(self, *args, **kwargs):
        super(CodeCalculator, self).__init__(*args, **kwargs)
        self.fields['liquied_narrow'].widget.attrs['disabled'] = 'disabled'
        self.fields['swu'].widget.attrs['disabled'] = 'disabled'
        self.fields['additive_type'].widget.attrs['disabled'] = 'disabled'
        self.fields['resin'].widget.attrs['disabled'] = 'disabled'
        self.fields['special_attribute'].widget.attrs['disabled'] = 'disabled'
        self.fields['special_requirement'].widget.attrs['disabled'] = 'disabled'       
        self.fields['ink_type'].widget.attrs['disabled'] = 'disabled'
        self.fields['color_type'].widget.attrs['disabled'] = 'disabled'
        self.fields['color_code_choice'].widget.attrs['disabled'] = 'disabled'
        self.fields['press'].widget.attrs['disabled'] = 'disabled'
        self.fields['mg_code'].widget.attrs['readonly'] = 'readonly'
        self.fields['ph_code'].widget.attrs['readonly'] = 'readonly'


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                Row(
                    Column('additive', css_class='form-group col-md-6 mb-0'), 
                    Column('liquied_narrow', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'  
                ),
                Row(
                    Column('swu', css_class='form-group col-md-6 mb-0'),
                    Column('additive_type', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row' 
                ),
                Row(
                    Column('resin', css_class='form-group col-md-6 mb-0'),
                    Column('special_attribute', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row' 
                ),
                Row(
                    Column('special_requirement', css_class='form-group col-md-6 mb-0'),
                    Column('ink_type', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row' 
                ),
                Row(
                    
                    Column('color_type', css_class='form-group col-md-3 mb-0'),
                    Column('color_code_choice', css_class='form-group col-md-3 mb-0'),
                    Column('press', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row' 
                ),
                Row(
                    Column('mg_code', readonly=True, css_class='form-group col-md-6 mb-0'),
                    Column('ph_code', readonly=True, css_class='form-group col-md-6 mb-0'),
                    css_class='form-row' 
                ),

            ),
            FormActions(
                Submit('submit', 'Save'),
                Reset('reset', 'Reset'),
            ),
        )
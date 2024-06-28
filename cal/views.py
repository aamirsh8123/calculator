from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, ListView, View
from cal.models import MaterialGroup, CreateCode, ColorCode
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import render, redirect
from cal.forms import MaterialGroupForm, CodeCalculator, ColorCodeForm
from django.contrib import messages
from django.db.models import QuerySet
from typing import Dict, Optional, Union
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MaterialGroupSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_user(user):
    return user.groups.filter(name='User').exists()



# Create your views here.


class IndexView(UserPassesTestMixin, TemplateView):
    template_name = 'calculator/index.html'

    def test_func(self):
        return is_user(self.request.user) or is_admin(self.request.user)

class MaterialList(UserPassesTestMixin, ListView):
    template_name = 'calculator/material/material_list.html'
    model = MaterialGroup
    context_object_name = 'items'
    paginate_by = 10  # Adjust the number as needed

    def test_func(self):
        return is_admin(self.request.user)


class MaterialDetail(UserPassesTestMixin, TemplateView):
    template_name = 'calculator/material/material_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('pk')  # 'pk' is the common convention for primary key in URLs
        context['item'] = get_object_or_404(MaterialGroup, pk=item_id)
        return context
    def test_func(self):
        return is_admin(self.request.user)
    
class MaterialUpdate(TemplateView):
    template_name = ''

@user_passes_test(is_admin)
def color_code_create(request):
    form = ColorCodeForm()
    if request.method == 'POST':
        form = ColorCodeForm(request.POST)
        if form.is_valid():
            form.save()
            # Use the name of the URL pattern instead of the template name
            messages.success(request, 'Data Save Successfully')
            form.helper.form_action = reverse('create_color_code')
    context = {'form': form}
    return render(request, 'calculator/material/create_color_code.html', context)

@user_passes_test(is_admin)
def material_creator(request):
    form = MaterialGroupForm()
    if request.method == 'POST':
        form = MaterialGroupForm(request.POST)
        if form.is_valid():

            instance = form.save()
            # Use the name of the URL pattern instead of the template name
            messages.success(request, 'Data Save Successfully')
            return redirect('material_detail', pk=instance.id)
    context = {'form': form}
    return render(request, 'calculator/material/create_item.html', context)


class PopulateFieldsView(UserPassesTestMixin, APIView):
    def get(self, request, *args, **kwargs):
        is_additive = request.GET.get('additive', None)
        swu_value = request.GET.get('swu', None)
        attribute_value = request.GET.get('special_attribute', None)
        
        default_fk = self.get_default_foreign_keys(is_additive, swu_value, attribute_value)
        context = {key: self.get_material_group(fk) for key, fk in default_fk.items()}
        serialized_context = self.serialize_context(context)
        
        # Use DRF's Response instead of JsonResponse
        return Response(serialized_context)

    def get_default_foreign_keys(self, is_additive, swu_value, attribute_value):
        default_fk = {
            'additive': 1,
            'liquied_narrow': None,
            'swu': None,
            'additive_type': None,
            'resin': None,
            'special_attribute': None,
            'special_requirement': None,
            'ink_type': None,
            'press': None,
        }

        if is_additive == '1':
            default_fk.update({'additive_type': 4, 'liquied_narrow': 2, 'swu': 3})
        elif is_additive == '2':
            default_fk.update({'liquied_narrow': 2, 'swu': 3})
            if swu_value in ['5', '6', '7']:
                default_fk.update(self.get_swu_specific_defaults(swu_value, attribute_value))

        return default_fk

    def get_swu_specific_defaults(self, swu_value: str, attribute_value: str) -> Dict[str, Optional[int]]:
        swu_defaults: Dict[str, Dict[str, int]] = {
            '5': {'additive_type': 5, 'resin': 8},
            '6': {'additive_type': 5, 'resin': 9},
            '7': {'additive_type': 6, 'resin': 10},
        }

        common_defaults: Dict[str, int] = {
            'special_attribute': 1,
            'ink_type': 11,
            'color_type': 13,
            'press': 14,
        }

        attribute_specific_defaults: Dict[str, Optional[int]] = {'special_requirement': 7} if attribute_value == '1' else {'special_requirement': None}

        defaults: Dict[str, Optional[int]] = {key: value for key, value in swu_defaults.get(swu_value, {}).items()}
        defaults.update({key: value for key, value in common_defaults.items()})
        defaults.update(attribute_specific_defaults)

        return defaults


    # Update your serialize_context method to use the serializer
    def serialize_context(self, context):
        return {
            key: MaterialGroupSerializer(queryset, many=True).data
            if isinstance(queryset, QuerySet) else queryset
            for key, queryset in context.items()
        }

    # Update your get_material_group method to use the serializer
    def get_material_group(self, fk):
        if fk is None:
            return []
        queryset = MaterialGroup.objects.filter(item_type_choice__id=fk)
        return MaterialGroupSerializer(queryset, many=True).data

    def test_func(self):
        return is_user(self.request.user) or is_admin(self.request.user)



@user_passes_test(is_admin or is_user)
def PopulateColorType(request):
    inkType = request.GET.get('color_type', None)
    if inkType:
        # Assuming ColorCode.objects.filter returns a QuerySet
        context = list(ColorCode.objects.filter(color_type_choice=inkType).values('id','color_code'))
    else:
        context = []
    return JsonResponse(context, safe=False)



class PopulateValue(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        additiveValue = request.GET.get('additive', None)
        liquiedNarrow = request.GET.get('liquied_narrow', None)
        swuValue = request.GET.get('swu', None)
        additivetypevalue = request.GET.get('additive_type', None)
        resinValue = request.GET.get('resin', None)
        specialAttributeValue = request.GET.get('special_attribute', None)
        specialRequirementValue = request.GET.get('special_requirement', None)
        inkTypeValue = request.GET.get('ink_type', None)
        colorValue = request.GET.get('color_type', None)
        colorCodeChoice = request.GET.get('color_code_choice', None)
        pressValue = request.GET.get('press', None)

        context = {
            'material_group': '',
            'product_hierarchy_a': '',
            'product_hierarchy_b': '',
        }
        if additiveValue == '1':
            if additiveValue:
                additive_group = MaterialGroup.objects.filter(id=additiveValue).values('material_group').first()
                if additive_group:
                    context['material_group'] = additive_group['material_group']
                print(f"Additive Value: {context['material_group']}")  # Debugging statement

            if liquiedNarrow:
                liquied_group = MaterialGroup.objects.filter(id=liquiedNarrow).values('material_group', 'product_hierarchy_a').first()
                if liquied_group:
                    context['material_group'] = liquied_group['material_group'] + '-' + context['material_group']
                    context['product_hierarchy_a'] = '0' + liquied_group['product_hierarchy_a']
                print(f"Liquid Narrow: {context['material_group']} + {context['product_hierarchy_a']}")  # Debugging statement , {context['product_hierarchy_a']}

            if swuValue:
                swu_hierarchy = MaterialGroup.objects.filter(id=swuValue).values('product_hierarchy_a').first()
                if swu_hierarchy:
                    context['product_hierarchy_a'] += swu_hierarchy['product_hierarchy_a']
                print(f"SWU Value: {context['product_hierarchy_a']}")  # Debugging statement

            if additivetypevalue:
                additive_type_group = MaterialGroup.objects.filter(id=additivetypevalue).values('material_group').first()
                if additive_type_group:
                    context['material_group'] += additive_type_group['material_group'] + 'X'
                print(f"Additive Type Value: {context['material_group']}")  # Debugging statement
        elif additiveValue == '2':
            if liquiedNarrow:
                liquied_group = MaterialGroup.objects.filter(id=liquiedNarrow).values('material_group', 'product_hierarchy_b').first()
                if liquied_group:
                    context['material_group'] = liquied_group['material_group'] + '-'
                    context['product_hierarchy_b'] = '0' + liquied_group['product_hierarchy_b']
                print(f"Liquid Narrow: {context['material_group']}")  # Debugging statement
            if swuValue:
                swu_hierarchy = MaterialGroup.objects.filter(id=swuValue).values('material_group', 'product_hierarchy_b').first()
                if swu_hierarchy:
                    context['material_group'] += swu_hierarchy['material_group']
                    context['product_hierarchy_b'] += swu_hierarchy['product_hierarchy_b']
                print(f"SWU Value: {context['product_hierarchy_b']}")  # Debugging statement

            if additivetypevalue:
                additive_type_group = MaterialGroup.objects.filter(id=additivetypevalue).values('material_group').first()
                if additive_type_group:
                    context['material_group'] += additive_type_group['material_group']
                print(f"Additive Type Value: {context['material_group']}")  # Debugging statement

            if resinValue:
                resin_group = MaterialGroup.objects.filter(id=resinValue).values('product_hierarchy_b').first()
                if resin_group:
                    context['product_hierarchy_b'] += resin_group['product_hierarchy_b']
                print(f"Resin Value: {context['product_hierarchy_b']}")  # Debugging statement
            if specialRequirementValue:
                requirement_group = MaterialGroup.objects.filter(id=specialRequirementValue).values('material_group').first()
                if requirement_group:
                    context['material_group'] += requirement_group['material_group']
                print(f"Special Requirement Value: {context['material_group']}")  # Debugging statement
            if specialAttributeValue == '1':
                if inkTypeValue:
                    ink_group = MaterialGroup.objects.filter(id=inkTypeValue).values('product_hierarchy_b').first()
                    if ink_group:
                        context['product_hierarchy_b'] += ink_group['product_hierarchy_b']
                    print(f"Resin Value: {context['product_hierarchy_b']}")  # Debugging statement
            elif specialAttributeValue == '2':
                if inkTypeValue:
                    ink_group = MaterialGroup.objects.filter(id=inkTypeValue).values('product_hierarchy_b').first()
                    if ink_group:
                        context['product_hierarchy_b'] += ink_group['product_hierarchy_b']
                    print(f"Resin Value: {context['product_hierarchy_b']}")  # Debugging statement
                if specialAttributeValue == '1':
                    if colorValue:
                        color_group = MaterialGroup.objects.filter(id=colorValue).values('material_group').first()
                        if color_group:
                            context['material_group'] += color_group['material_group']
                        print(f"Color Value: {context['material_group']}")  # Debugging statement
                elif specialAttributeValue == '2':                            
                    if colorCodeChoice:
                        color_choice_group = ColorCode.objects.filter(id=colorCodeChoice).values('material_group').first()
                        if color_choice_group:
                            context['material_group']+=color_choice_group['material_group']
                        print(f"Color Code Choice: {context['material_group']}")
            if pressValue:
                press_group = MaterialGroup.objects.filter(id=pressValue).values('material_group', 'product_hierarchy_b').first()
                if press_group:
                    context['material_group'] += press_group['material_group']
                    context['product_hierarchy_b'] += press_group['product_hierarchy_b']
                print(f"Press Value: {context['material_group']} + {context['product_hierarchy_b']}")  # Debugging statement

        return JsonResponse(context)
    
    def test_func(self):
        return is_user(self.request.user) or is_admin(self.request.user)



class CodeList(UserPassesTestMixin, ListView):
    template_name = 'calculator/code/code_list.html'
    model = CreateCode
    context_object_name = 'items'
    paginate_by = 10

    def test_func(self):
        return is_user(self.request.user) or is_admin(self.request.user)

class CodeDetail(UserPassesTestMixin, TemplateView):
    template_name = 'calculator/code/code_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('pk')  # 'pk' is the common convention for primary key in URLs
        context['item'] = get_object_or_404(CreateCode, pk=item_id)
        return context
    
    def test_func(self):
        return is_user(self.request.user) or is_admin(self.request.user)

@user_passes_test(is_admin or is_user)
def mg_calculator(request):
    form = CodeCalculator()
    if request.method == 'POST':
        form = CodeCalculator(request.POST)
        if form.is_valid():
            instance = form.save()
            # Use the name of the URL pattern instead of the template name
            messages.success(request, 'Data Save Successfully')
            return redirect('code_detail', pk=instance.id)
    context = {'form': form}
    return render(request, 'calculator/code/calculator.html', context)




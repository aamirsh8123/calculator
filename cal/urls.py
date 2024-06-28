from django.urls import path, include
from cal.views import IndexView, MaterialList, MaterialDetail, PopulateFieldsView, PopulateValue, CodeList, CodeDetail
from . import views


urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('materials/',MaterialList.as_view(),name="material_list"),
    path('detail/<int:pk>',MaterialDetail.as_view(),name="material_detail"),
    path('create/materialgroup/',views.material_creator, name='create_item'),
    path('create/code/',views.mg_calculator, name='create_code'),

    path('codes/',CodeList.as_view(),name='code_list'),
    path('code/<int:pk>',CodeDetail.as_view(),name="code_detail"),    
    path('populate-fields/',PopulateFieldsView.as_view(), name='populate-fields'),
    path('get_value/',PopulateValue.as_view(),name='get-value'),
    path('get_color_choice',views.PopulateColorType,name='get-color-choice'),
    path('color/code/',views.color_code_create, name='create_color_code'),
    # path('accounts/',include('django.contrib.auth.urls')),
]

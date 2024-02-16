from django.urls import path
from . import views

urlpatterns = [
    path('total_list/', views.total_list),
    path('total_list_data/', views.total_list__data),
    path('hw4/', views.hw4),
    path('hw4_data/', views.hw4_data),
    path('hw4_S08_plot/', views.hw4_S08_plot),
    path('hw4_S09_plot/', views.hw4_S09_plot),
]
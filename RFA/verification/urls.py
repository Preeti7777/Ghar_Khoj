from django.urls import path
from . import views

urlpatterns = [

    path("",views.verification_list,
         name="verification_list"),
    path("<int:pk>/",views.verification_detail,
         name="verification_detail"),
    path("<int:pk>/approve/",
         views.approve_property, name="approve_property"),
    path("<int:pk>/reject/",
         views.reject_property,name="reject_property"),
]

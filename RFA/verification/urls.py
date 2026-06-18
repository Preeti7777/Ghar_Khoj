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
     path(
    "certificate-verification/",
    views.certificate_verification_list,
    name="certificate_verification_list"
     ),

     path(
     "certificate-verification/<int:user_id>/",
     views.certificate_verification_detail,
     name="certificate_verification_detail"
     ),

     path(
     "certificate-verification/<int:user_id>/approve/",
     views.approve_certificate,
     name="approve_certificate"
     ),

     path(
     "certificate-verification/<int:user_id>/reject/",
     views.reject_certificate,
     name="reject_certificate"
     ),
]

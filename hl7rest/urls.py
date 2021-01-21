from . import views
from django.urls import path

urlpatterns = [
    path('form.html', views.render_form_View, name='form1'),
    path('hl7', views.hl7_web_view ,name='hl7')
]
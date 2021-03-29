from django.urls import path

from main import views

urlpatterns = [
	path('', views.get_index_View_input),
	path('postbackscript/', views.postback),
	path('output/', views.output_View,  name='output'),
]

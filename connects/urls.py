from . import views
from django.urls import path

urlpatterns = [

	path('create/', views.create, name='create'),
	path('post_create/', views.post_create, name='post_create'),


	path('', views.index, name='index'),
	path('details/', views.details, name='details'),
	path('home/', views.home, name='home'),
	path('profile/', views.profile, name='profile'),
	path('test/', views.test, name='test'),
	path('news/', views.news, name='news'),


]
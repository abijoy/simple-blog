
from django.urls import path, include
from . import views
from blog import views as blog_views
from django.contrib.auth import views as auth_views


app_name = 'cadmin'

urlpatterns = [
	path('post/add/', views.post_add, name='post_add'),
	path('post/update/<int:pk>/', views.post_update, name='post_update'),
	
	path('login/',
		auth_views.login,
		{'template_name': 'cadmin/login.html'},
		name='login'
	),
	path('logout/',
		auth_views.logout,
		{'template_name': 'cadmin/logout.html'},
		name='logout'
	),
	path('', views.home, name='home'),
	path('password-change-done/',
		auth_views.password_change_done,
		name='password_change_done'
	),
	path('password-change/',
		auth_views.password_change, 
		{'post_change_redirect': 'password_change_done'},
		name='password_change'
	),
	path('register/', views.register, name='register'),
	
]


from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
	# path('', views.index, name='index'),
	path('', views.post_list, name='post_list'),
	# path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/<int:pk>/<post_slug>/', views.post_detail, name='post_detail'),
	path('category/<category_slug>/', views.posts_by_category, name='posts_by_category'),
	path('tag/<tag_slug>/', views.posts_by_tag, name='posts_by_tag'),
	path('author/<author_slug>/', views.posts_by_author, name='posts_by_author'),
	path('blog/', views.test_redirect, name='test_redirect'),
	path('feedback/', views.feedback, name='feedback'),
	path('signup/', views.signup, name='signup'),
	path('track/', views.track_user, name='track_user'),
	path('stop-tracking/', views.stop_tracking, name='stop_tracking'),
	path('test-session/', views.test_session, name='test_session'),
	path('test-delete/', views.test_delete, name='test_delete'),
	path('save-session-data/', views.save_session_data, name='save_session_data'),
	path('access-session-data/', views.access_session_data, name='access_session_data'),
	path('delete-session-data/', views.delete_session_data, name='delete_session_data'),
	path('lousy-login/', views.lousy_login, name='lousy_login'),
	path('lousy-logged-inX/', views.lousy_logged_in, name='lousy_logged_in'),
	path('lousy-logout/', views.lousy_logout, name='lousy_logout'),
	path('login/', views.login, name='login'),
	path('admin_page/', views.admin_page, name='admin_page'),
	path('logout/', views.logout, name='logout'),

]
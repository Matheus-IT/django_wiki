from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
	path("", views.index, name="index"),
	path('search/', views.search, name='search'),
	path('new_entry/', views.new_entry, name='create_new_entry'),
	path('confirm_new_entry/', views.confirm_new_entry, name='confirm_new_entry'),
	path('edit_entry/<str:entry_title>/', views.edit_entry, name='edit_entry'),
	path('save_changes/<str:entry_title>/', views.save_changes_after_edit, name='save_changes'),
	path('random_page/', views.random_page, name='random_page'),
	path('<str:entry_title>/', views.entry_page, name='entry_page')
]

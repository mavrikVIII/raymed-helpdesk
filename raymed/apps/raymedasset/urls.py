from django.urls import path
from . import views
from django.contrib.auth import views as standart_views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

app_name = "raymedasset"

urlpatterns = [

    path('search_for_name', views.search_for_name, name = 'search_for_name'),
    path('<int:person_id>/', views.detail_person, name = 'detail_person'),
    path('search_for_type_device', views.search_for_type_device, name = 'search_for_type_device'),
    path('add_person_page', views.add_person_page , name = "add_person_page"),
    path('add_device_page', views.add_device_page, name = 'add_device_page'),
    path('search_for_number_account',views.search_for_number_account, name = 'search_for_number_account'),
    path('see_all_device', views.see_all_device, name = 'see_all_device'),
    path('<int:person_id>/add_device_page/', views.add_device_page_this_person, name = 'add_device_page_this_person'),
    path('transfer_device_<int:device_id>', views.transfer_device, name = 'transfer_device'),
    path('transfer_subdevice_<int:subdevice_id>', views.transfer_subdevice, name = 'transfer_subdevice'),
    path('transfer_device_<int:device_id>/delete_device', views.delete_device, name = 'delete_device'),
    path('transfer_subdevice_<int:subdevice_id>/delete_subdevice', views.delete_subdevice, name = 'delete_subdevice'),
    path('see_all_person', views.see_all_person, name = 'see_all_person'),
    path('edit_person_<int:person_id>', views.edit_person, name = 'edit_person'),
    path('search', views.search, name = 'search'),
    path('admin/', admin.site.urls),
    path('see_device_for_number_account_<str:number_account>', views.see_device_for_number_account, name = 'see_device_for_number_account'),
    path('see_device_without_person', views.see_device_without_person, name = 'see_device_without_person'),
    path('search_for_department', views.search_for_department, name = 'search_for_department'),
    path('see_all_this_department_<str:name_department>', views.see_all_this_department, name = 'see_all_this_department'),
    path('see_all_this_type_device_<str:type_device>', views.see_all_this_type_device, name = 'see_all_this_type_device'),
    path('add_subdevice_<int:device_id>', views.add_subdevice, name = 'add_subdevice'),
    path('see_all_subdevice', views.see_all_subdevice, name = 'see_all_subdevice'),
    path('history_move_this_device_<int:device_id>', views.history_move_this_device, name = 'history_move_this_device'),
    path('test', views.test, name = 'test'),



]

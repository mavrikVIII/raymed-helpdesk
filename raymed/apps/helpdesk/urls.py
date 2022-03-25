from django.urls import path
from . import views
from django.contrib.auth import views as standart_views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

app_name = "helpdesk"

urlpatterns = [

    # path('', views.main_index, name = 'main_index'),
    # path('post_error_<int:device_id>', views.post_error, name ='post_error'),
    path('views_errors_for_this_user<int:user_id>', views.views_errors_for_this_user, name ='views_errors_for_this_user'),
    path('view_all_errors', views.view_all_errors, name ='view_all_errors'),
    path('edit_error_<int:error_id>', views.edit_error, name ='edit_error'),
    path('index_for_buh_<int:user_id>', views.index_for_buh, name ='index_for_buh'),
    path('detail_error_<int:error_id>', views.detail_error, name ='detail_error'),
    # path('post_other_error', views.post_other_error, name ='post_other_error'),
    # path('edit_other_error_<int:error_id>', views.edit_other_error, name ='edit_other_error'),
    path('post_global_error', views.post_global_error, name ='post_global_error'),

]

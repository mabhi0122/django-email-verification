from django.urls import path
from . import views


urlpatterns = [

    path('', views.index_view, name= 'index'),
    path('register/',views.register_user, name='register'),
    path('activate/<uidb64>/<token>/',views.activate_user, name= 'activate'),
    path('login/', views.login_user, name= 'login'),
    path('logout/', views.logout_user, name= 'logout'),

]

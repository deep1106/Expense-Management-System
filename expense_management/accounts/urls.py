from . import views
from django.urls import path

urlpatterns = [
    path('',views.director_signup,name='director_signup'),
    path('login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='user_logout'),
    path('add-user/',views.add_user,name='add_user'),
]

from django.urls import path 
from django.contrib import admin
from .views import homepage,Registration,Login,aboutpage,category_list,quiz_view,result_view,gameover_view,leaderboard,user_logout,profile_view,forgot_password,reset_password

urlpatterns =[
    path('',homepage,name='homepage'),
    path('registration/', Registration.as_view(),name ='registration'),
    path('login/',Login.as_view(),name="login"),
    path('about/',aboutpage,name='aboutpage'),
    path('categories/', category_list, name='categories'),
    path('quiz/<int:category_id>/<int:q_no>/', quiz_view, name='quiz'),
    path('result/<int:category_id>/<int:solved>/', result_view, name='result'),
    path('gameover/<int:category_id>/<int:solved>/', gameover_view, name='gameover'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('logout/',user_logout,name='logout'),
    path('profile/', profile_view, name='profile'),
    path('forgot-password/',forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/', reset_password, name='reset_password'),

]
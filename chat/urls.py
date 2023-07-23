from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<str:room>/', views.room, name="room"),
    path('checkview', views.checkview, name="checkview"),
    path('send/<str:room>/', views.send, name="send"),
    path('getMessage/<str:room>/', views.getMessage, name="getMessage"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("<str:room>/director/", views.director, name="director"),
    path("getrooms/<str:room>/", views.getrooms, name="getrooms"),
    path("roomdirect/<str:room>/", views.roomdirect, name="roomdirect"),
]

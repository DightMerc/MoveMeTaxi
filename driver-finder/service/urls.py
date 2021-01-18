from django.urls import path

from . import views

urlpatterns = [
    path('driver/', views.FindClosestDriver.as_view()),
    # path('<str:room_name>/', views.room, name='room'),
]
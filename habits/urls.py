# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitsList

app_name = 'habits'

router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('public/', PublicHabitsList.as_view(), name='public-habits'),
]

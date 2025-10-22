from rest_framework import viewsets, generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'place', 'reward']
    ordering_fields = ['time', 'created_at']

    def get_queryset(self):
        # CRUD доступ только к своим привычкам
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PublicHabitsList(generics.ListAPIView):
    """
    Список публичных привычек (read-only)
    """
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
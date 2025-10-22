from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'users'

#router = DefaultRouter()
#router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    #path('', include(router.urls)),
    #path('payments/', PaymentListView.as_view(), name='payment-list'),
    ## Регистрация и JWT
    #path('register/', RegisterView.as_view(), name='register'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ## Payment
    #path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    #path('payment/success/', PaymentSuccessView.as_view(), name='payment-success'),
    #path('payment/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
]
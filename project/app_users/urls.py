from django.urls import path
from app_users.views import (
    CustomLoginListCreateAPIView,
    CustomUserCodeConfirmFormView,
    CustomUserRetrieveAPIView,
    SimulateSendingCodeTemplateView,
    CustomLogoutRetrieveAPIView
)


app_name = 'app_users'


urlpatterns = [
    path('<int:pk>/', CustomUserRetrieveAPIView.as_view(), name='user-info'),
    path('login/', CustomLoginListCreateAPIView.as_view(), name='login'),
    path('logout/', CustomLogoutRetrieveAPIView.as_view(), name='logout'),
    path('login/confirm/<int:pk>/', CustomUserCodeConfirmFormView.as_view(), name='confirm'),
    path('login/confirm/<int:pk>/sending_code/', SimulateSendingCodeTemplateView.as_view(), name='sending-code'),
]

from django.urls import path
from . import views as v

urlpatterns = [
    path('login', v.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register', v.register_user, name='register'),
    path('profile/<int:pk>', v.get_user_profile_pk, name='get_user_id'),
    path('user-list', v.user_list, name='user-list'),
]

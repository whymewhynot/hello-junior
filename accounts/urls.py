from django.urls import path
from accounts.views import LoginOrRegisterView, logout_view, UserProfileView, \
    MyPasswordChangeView, MyPasswordResetView, MyPassResetConfirmView, \
    add_or_remove_favorite, favorites_view

urlpatterns = [
    path('login/', LoginOrRegisterView.as_view(), name='login'),
    path('register/', LoginOrRegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('pwd-reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('pwd-reset/<uidb64>/<token>/', MyPassResetConfirmView.as_view(), name='password_reset_confirm'),
    path('add_remove/<int:id>', add_or_remove_favorite, name='add_remove'),
    path('favorites/', favorites_view, name='favorites')
]
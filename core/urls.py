from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, LoginView, RegisterView, DashboardView, AdminDashboardView, CampaignDetailView, CreateCampaignView, CategoryDetailView, ForgotPasswordRequestView, ForgotPasswordVerifyView, ForgotPasswordResetView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/new/', CreateCampaignView.as_view(), name='create_campaign'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    # Password Reset
    path('password-reset/', ForgotPasswordRequestView.as_view(), name='password_reset_request'),
    path('password-reset/verify/', ForgotPasswordVerifyView.as_view(), name='password_reset_verify'),
    path('password-reset/confirm/', ForgotPasswordResetView.as_view(), name='password_reset_confirm'),
]


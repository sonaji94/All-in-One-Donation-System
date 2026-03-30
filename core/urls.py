from django.urls import path
from django.contrib.auth.views import LogoutView
<<<<<<< HEAD
from .views import HomeView, LoginView, RegisterView, DashboardView, AdminDashboardView, CampaignDetailView, CreateCampaignView, CategoryDetailView, ForgotPasswordRequestView, ForgotPasswordVerifyView, ForgotPasswordResetView
=======
<<<<<<< HEAD
from .views import HomeView, LoginView, RegisterView, DashboardView, AdminDashboardView, CampaignDetailView, CreateCampaignView
=======
from .views import HomeView, LoginView, RegisterView, DashboardView, CampaignDetailView, CreateCampaignView, CategoryDetailView
>>>>>>> c7c1a19dd373c1bfd37bb625fc49b976f6ae5852
>>>>>>> 11b04389547943f6cd409ae4f74ccc304e0b5e71

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
<<<<<<< HEAD
=======
<<<<<<< HEAD
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/new/', CreateCampaignView.as_view(), name='create_campaign'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
=======
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
>>>>>>> 11b04389547943f6cd409ae4f74ccc304e0b5e71
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/new/', CreateCampaignView.as_view(), name='create_campaign'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
<<<<<<< HEAD
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    # Password Reset
    path('password-reset/', ForgotPasswordRequestView.as_view(), name='password_reset_request'),
    path('password-reset/verify/', ForgotPasswordVerifyView.as_view(), name='password_reset_verify'),
    path('password-reset/confirm/', ForgotPasswordResetView.as_view(), name='password_reset_confirm'),
]

=======
>>>>>>> c7c1a19dd373c1bfd37bb625fc49b976f6ae5852
]
>>>>>>> 11b04389547943f6cd409ae4f74ccc304e0b5e71

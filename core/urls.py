from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, LoginView, RegisterView, DashboardView, AdminDashboardView, CampaignDetailView, CreateCampaignView, CategoryDetailView, CategoryListView, ForgotPasswordRequestView, ForgotPasswordVerifyView, ForgotPasswordResetView, MyDonationsView, MyTicketsView, RaiseTicketView, AccountSettingsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/donations/', MyDonationsView.as_view(), name='my_donations'),
    path('dashboard/tickets/', MyTicketsView.as_view(), name='my_tickets'),
    path('dashboard/tickets/raise/', RaiseTicketView.as_view(), name='raise_ticket'),
    path('dashboard/account/', AccountSettingsView.as_view(), name='account_settings'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
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

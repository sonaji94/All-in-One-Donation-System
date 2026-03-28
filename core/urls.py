from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, LoginView, RegisterView, DashboardView, CampaignDetailView, CreateCampaignView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/new/', CreateCampaignView.as_view(), name='create_campaign'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

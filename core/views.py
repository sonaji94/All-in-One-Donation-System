from django.views.generic import TemplateView, DetailView, FormView, CreateView, ListView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count
from accounts.models import User
from donations.models import Donation
from campaigns.models import Campaign, Category, CampaignProof
from campaigns.forms import CampaignForm, CampaignProofForm
from .models import SupportTicket
from .forms import SupportTicketForm
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm, OTPForgotPasswordForm, OTPVerifyForm, SetNewPasswordForm
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trending_campaigns'] = Campaign.objects.filter(
            status=Campaign.Status.ACTIVE, approved=True
        ).order_by('-raised_amount')[:3]
        context['categories'] = Category.objects.all()[:4]
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaigns'] = self.object.campaigns.filter(
            status=Campaign.Status.ACTIVE,
            approved=True
        ).order_by('-raised_amount')
        context['all_categories'] = Category.objects.all()[:4] # Consistent with home page
        return context

class LoginView(AuthLoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class BaseDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['my_campaigns'] = Campaign.objects.filter(owner=user)
        context['my_donations'] = Donation.objects.filter(
            donor=user, 
            status=Donation.Status.SUCCESS
        ).order_by('-created_at')
        return context

class DashboardView(BaseDashboardView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'campaigns'
        return context

class MyDonationsView(BaseDashboardView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'donations'
        return context

class MyTicketsView(BaseDashboardView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'tickets'
        context['support_tickets'] = SupportTicket.objects.filter(user=self.request.user)
        context['ticket_form'] = SupportTicketForm()
        return context

class RaiseTicketView(LoginRequiredMixin, CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        ticket = form.save()
        messages.success(self.request, f"Ticket {ticket.ticket_id} has been raised successfully! Our team will review it shortly.")
        return redirect('my_tickets')
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error raising your ticket. Please check the details and try again.")
        return redirect('my_tickets')

class AccountSettingsView(BaseDashboardView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'settings'
        return context

class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'campaign_detail.html'
    context_object_name = 'campaign'

class CreateCampaignView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'create_campaign.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['proof_form'] = CampaignProofForm(self.request.POST, self.request.FILES, prefix='proof')
        else:
            data['proof_form'] = CampaignProofForm(prefix='proof')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        proof_form = context['proof_form']

        if form.is_valid() and proof_form.is_valid():
            form.instance.owner = self.request.user
            self.object = form.save()
            
            # Save the proof
            proof = proof_form.save(commit=False)
            if proof.document: # Only save if a document was actually uploaded
                proof.campaign = self.object
                proof.save()

            return redirect('campaign_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_admin_role() or self.request.user.is_superuser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate totals
        context['total_collected'] = Campaign.objects.aggregate(total=Sum('raised_amount'))['total'] or 0
        context['total_campaigns'] = Campaign.objects.count()
        context['total_users'] = User.objects.count()
        
        # Seekers (users who have created campaigns)
        context['seekers'] = User.objects.filter(campaigns__isnull=False).distinct().annotate(
            total_raised=Sum('campaigns__raised_amount'),
            campaign_count=Count('campaigns')
        ).order_by('-total_raised')
        
        return context

class ForgotPasswordRequestView(FormView):
    template_name = 'accounts/password_reset_request.html'
    form_class = OTPForgotPasswordForm
    success_url = reverse_lazy('password_reset_verify')

    def form_valid(self, form):
        phone = form.cleaned_data['phone_number']
        user = User.objects.get(phone_number=phone)
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        user.otp_code = otp
        user.otp_expiry = timezone.now() + timedelta(minutes=10)
        user.save()

        # MOCK SMS SENDING
        print("\n" + "="*40)
        print(f"MOCK SMS SENT TO {phone}")
        print(f"YOUR OTP CODE IS: {otp}")
        print("="*40 + "\n")
        
        self.request.session['reset_phone'] = phone
        messages.success(self.request, f"OTP sent to {phone}. [DEBUG] YOUR OTP IS: {otp}")
        return super().form_valid(form)

class ForgotPasswordVerifyView(FormView):
    template_name = 'accounts/password_reset_verify.html'
    form_class = OTPVerifyForm
    success_url = reverse_lazy('password_reset_confirm')

    def form_valid(self, form):
        otp = form.cleaned_data['otp_code']
        phone = self.request.session.get('reset_phone')
        
        if not phone:
            return redirect('password_reset_request')
        
        try:
            user = User.objects.get(phone_number=phone)
            if user.otp_code == otp and user.otp_expiry > timezone.now():
                user.otp_code = None # Clear OTP after verification
                user.save()
                return super().form_valid(form)
            else:
                form.add_error('otp_code', "Invalid or expired OTP.")
                return self.form_invalid(form)
        except User.DoesNotExist:
            return redirect('password_reset_request')

class ForgotPasswordResetView(FormView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = SetNewPasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        phone = self.request.session.get('reset_phone')
        if not phone:
            return redirect('password_reset_request')
        
        try:
            user = User.objects.get(phone_number=phone)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            
            del self.request.session['reset_phone']
            messages.success(self.request, "Password reset successful. You can now log in with your new password.")
            return super().form_valid(form)
        except User.DoesNotExist:
            return redirect('password_reset_request')


from django.views.generic import TemplateView, DetailView, FormView, CreateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from campaigns.models import Campaign, Category, CampaignProof
from campaigns.forms import CampaignForm, CampaignProofForm
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trending_campaigns'] = Campaign.objects.filter(status=Campaign.Status.ACTIVE).order_by('-raised_amount')[:3]
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
        login(self.request, self.object)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['my_campaigns'] = Campaign.objects.filter(owner=self.request.user)
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

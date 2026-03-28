from django import forms
from .models import Campaign, CampaignProof

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
<<<<<<< HEAD
        fields = ('title', 'description', 'goal_amount', 'category', 'location', 'image')
=======
        fields = ('title', 'description', 'goal_amount', 'category', 'location', 'image', 'payment_qr_code')
>>>>>>> c7c1a19dd373c1bfd37bb625fc49b976f6ae5852
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class CampaignProofForm(forms.ModelForm):
    class Meta:
        model = CampaignProof
        fields = ('document', 'document_type', 'description')

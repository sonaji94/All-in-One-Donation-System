from django import forms
from .models import Campaign, CampaignProof

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('title', 'description', 'goal_amount', 'category', 'location', 'image')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class CampaignProofForm(forms.ModelForm):
    class Meta:
        model = CampaignProof
        fields = ('document', 'document_type', 'description')

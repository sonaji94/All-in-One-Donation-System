from django.contrib import admin
from .models import Category, Campaign, CampaignProof

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class CampaignProofInline(admin.TabularInline):
    model = CampaignProof
    extra = 0

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'status', 'approved', 'goal_amount')
    list_filter = ('status', 'approved', 'category')
    search_fields = ('title', 'owner__username')
    list_editable = ('status', 'approved')
    inlines = [CampaignProofInline]
    actions = ['approve_campaigns']

    @admin.action(description='Approve selected campaigns (sets status ACTIVE and approved True)')
    def approve_campaigns(self, request, queryset):
        queryset.update(approved=True, status='ACTIVE')

@admin.register(CampaignProof)
class CampaignProofAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'document_type', 'is_verified')
    list_filter = ('is_verified', 'document_type')
    list_editable = ('is_verified',)

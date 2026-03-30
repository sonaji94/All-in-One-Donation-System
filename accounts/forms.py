from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    phone_number = forms.CharField(required=True, max_length=15)
    
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        login_id = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if login_id and password:
            # Try to find user by email OR phone_number
            user = User.objects.filter(email=login_id).first() or \
                   User.objects.filter(phone_number=login_id).first()
            
            if user:
                # authenticate still expects the username field (email in our case)
                self.user_cache = authenticate(self.request, email=user.email, password=password)
            
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid Email/Mobile or password."
                )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class OTPForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="Mobile Number")

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("No user found with this mobile number.")
        return phone

class OTPVerifyForm(forms.Form):
    otp_code = forms.CharField(max_length=6, min_length=6, label="Enter 6-Digit OTP")

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

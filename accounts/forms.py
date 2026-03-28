from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'password')

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
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct email and password. Note that both fields may be case-sensitive."
                )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

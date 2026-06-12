"""Registration and profile-editing forms with Bootstrap styling."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    """Sign-up form: username, email, password x2, phone, address."""
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to every field
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit)
        # Store extra info on the auto-created profile
        user.profile.phone = self.cleaned_data.get('phone', '')
        user.profile.address = self.cleaned_data.get('address', '')
        user.profile.save()
        return user


class LoginForm(AuthenticationForm):
    """Login form with Bootstrap classes."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    """Edit phone & address from the profile page."""
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address']
        widgets = {'address': forms.Textarea(attrs={'rows': 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        profile = super().save(commit)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        return profile

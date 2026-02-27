from django import forms
from django.contrib.auth.models import User
from .models import Profile, DailyCalorie


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'age', 'gender', 'height', 'weight']


class DailyCalorieForm(forms.ModelForm):
    class Meta:
        model = DailyCalorie
        fields = ['item_name', 'calorie_consumed']
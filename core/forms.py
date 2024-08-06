from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Review

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'phone_number', 'review', 'email', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone_number


class PhoneNumberForm(forms.Form):
    """
    Form for collecting a visitor's phone number.
    """
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )

class FullReviewForm(forms.ModelForm):
    """
    Form for collecting full information from a visitor who has not yet reviewed.
    """
    name = forms.CharField(
        max_length=100, 
        required=True, 
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    email = forms.EmailField(
        required=False, 
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email (optional)'})
    )

    class Meta:
        model = Review
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Enter your review here...'}),
        }

class SimpleReviewForm(forms.ModelForm):
    """
    Form for updating an existing review.
    """
    class Meta:
        model = Review
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Update your review here...'}),
        }

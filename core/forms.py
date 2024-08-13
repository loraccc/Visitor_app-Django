from django import forms
from .models import CustomUser,Review

from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'phone_number', 'review', 'email', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone_number

def validate_phone_number_length(value):
    """
    Validator to ensure that the phone number is exactly 10 digits long.
    """
    if len(str(value)) != 10:
        raise ValidationError(
            'Phone number must be exactly 10 digits long.',
            code='invalid_phone_number_length'
        )
class PhoneNumberForm(forms.Form):
    """
    Form for collecting a visitor's phone number.
    """
    phone_number = forms.IntegerField(
        required=True, 
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number',
            'type': 'tel',  # Use type 'tel' for numeric input on mobile devices
        }),
        validators=[validate_phone_number_length]
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
    department = forms.ChoiceField(
        choices=Review.DEPARTMENT_CHOICES, 
        required=True,
        label='Department',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    purpose = forms.ChoiceField(
        choices=Review.PURPOSE_CHOICES, 
        required=True,
        label='Purpose',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    other_purpose = forms.CharField(
        max_length=255,
        required=False,
        label='If Other, please specify',
        widget=forms.TextInput(attrs={'placeholder': 'Enter additional details here...'}),
    )

    class Meta:
        model = Review
        fields = ['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Enter your review here...'}),
        }

    def __init__(self, *args, **kwargs):
        super(FullReviewForm, self).__init__(*args, **kwargs)
        # Ensure all fields have consistent styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        # Set the order of the fields explicitly
        self.order_fields(['name', 'phone_number', 'email', 'department', 'purpose', 'other_purpose', 'review'])

        # Initial hide the 'other_purpose' field
        if self.instance and self.instance.purpose != 'Other':
            self.fields['other_purpose'].widget.attrs['style'] = 'display:none;'

    def clean(self):
        cleaned_data = super().clean()
        purpose = cleaned_data.get('purpose')
        other_purpose = cleaned_data.get('other_purpose')

        if purpose == 'Other' and not other_purpose:
            self.add_error('other_purpose', 'Please specify your purpose if "Other" is selected.')
        elif purpose != 'Other' and other_purpose:
            self.add_error('other_purpose', 'The additional details should only be filled if "Other" is selected.')

        return cleaned_data

class SimpleReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']  # Only the fields you want to update
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Update your review here...'}),
        }

    def clean_review(self):
        review = self.cleaned_data.get('review', '').strip()
        if not review:
            raise forms.ValidationError("Review cannot be empty.")
        return review

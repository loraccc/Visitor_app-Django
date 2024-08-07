from .models import User, User_number, Review_page
from django import forms

class NumberForm(forms.ModelForm):
    class Meta:
      model = User_number
      fields = ['mobile_number']

class UserForm(forms.ModelForm):
   class Meta:
      model = User
      fields = ['username', 'email', 'review']

class  ReviewForm(forms.ModelForm):
   class Meta:
      model = Review_page
      fields = ['review']
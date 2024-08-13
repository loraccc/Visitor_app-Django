from .models import Review

from .forms import *

import qrcode

from PIL import Image

from io import BytesIO

from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True  
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        """If the form is valid, redirect to the success URL."""
        messages.success(self.request, "You have successfully logged in.")  # Add a success message
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, "Invalid username or password.")  # Add an error message
        return self.render_to_response(self.get_context_data(form=form))


def home(request):
    return render(request, 'home.html') 

# def submit_review(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')

#         # Check if the phone number exists
#         review_instance = Review.objects.filter(phone_number=phone_number).first()

#         if review_instance:
#             # Handle existing review
#             form = SimpleReviewForm(request.POST, instance=review_instance)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('')
#             else:
#                 # If form is not valid, re-render the simple form
#                 return render(request, 'simple_review.html', {'form': form})

#         else:
#             # Handle new review
#             form = FullReviewForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('')
#             else:
#                 # If form is not valid, re-render the full review form
#                 return render(request, 'submit_review.html', {'form': form})
    
#     # Render phone number form if not a POST request or phone number not found
#     form = PhoneNumberForm()
#     return render(request, 'phone_number.html', {'form': form})

def submit_review(request):
    if request.method == 'POST':
        # Process form submission
        phone_number = request.POST.get('phone_number', None)
        if not phone_number:
            # If phone number is not provided, render the phone number form
            form = PhoneNumberForm()
            return render(request, 'phone_number.html', {'form': form})

        try:
            # Check if the user already exists
            user_review = Review.objects.get(phone_number=phone_number)
            # User has reviewed, provide option to update review
            form = SimpleReviewForm(request.POST, instance=user_review)
            print(request.POST,'helloooooooo')
            if form.is_valid():
                print(form.cleaned_data)
                form.save()
                return redirect('home')
            else:
                print(form.errors) 
                # Render the simple review form with errors
                return render(request, 'simple_review.html', {'form': form, 'user_review': user_review})
        except Review.DoesNotExist:
            # User has not reviewed, collect full info
            form = FullReviewForm(request.POST)
            if form.is_valid():
                # Save new user and review
                Review.objects.create(
                    name=form.cleaned_data['name'],
                    phone_number=form.cleaned_data['phone_number'],
                    email=form.cleaned_data['email'],
                    review=form.cleaned_data['review']
                )
                return HttpResponse("Thank you for submitting your review!")
            else:
                # Render the full review form with errors
                return render(request, 'submit_review.html', {'form': form, 'phone_number': phone_number})
    else:
        # Display phone number entry form
        form = PhoneNumberForm()
        return render(request, 'phone_number.html', {'form': form})


def review_qr(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'review_qr.html', {'review': review})

def see_qr(request):

    return render(request, 'qr.html')



def visitor_statistics(request):
    today = timezone.now().date()
    total_visitors_today = Review.objects.filter(created_at__date=today).count()
    reviews_today = Review.objects.filter(created_at__date=today)
    return render(request, 'visitor_statistics.html', {
        'total_visitors_today': total_visitors_today,
        'reviews_today': reviews_today,
    })
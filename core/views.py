from .models import Review

from .forms import *

import qrcode

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
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page.
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True  # Automatically redirect authenticated users
    success_url = reverse_lazy('home')  # URL to redirect to after successful login

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


def submit_review(request):
    # Retrieve phone number from GET or POST
    phone_number = request.POST.get('phone_number') or request.GET.get('phone_number')

    if request.method == 'POST':
        if not phone_number:
            # Render the phone number form if the number is not provided
            form = PhoneNumberForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data['phone_number']
                return redirect(f'?phone_number={phone_number}')
            else:
                return render(request, 'phone_number.html', {'form': form})

        try:
            # Check if the phone number exists in the database
            user_review = Review.objects.get(phone_number=phone_number)
            # User has reviewed, provide option to update review
            form = SimpleReviewForm(request.POST, instance=user_review)
            if form.is_valid():
                review_text = form.cleaned_data.get('review', '').strip()
                if not review_text:
                    return render(request, 'simple_review.html', {'form': form, 'errors': {'review': ['Review cannot be empty.']}})
                
                form.save()
                print("Review updated successfully.")
                return render(request, 'simple_review.html', {'form': form, 'message': "Thank you for updating your review!"})
            else:
                # Render the form again if not valid and show errors
                print("Form errors:", form.errors)
                return render(request, 'simple_review.html', {'form': form, 'user_review': user_review, 'errors': form.errors})
        except Review.DoesNotExist:
            # If no review exists, create a new one
            form = FullReviewForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'submit_review.html', {'form': form, 'message': "Thank you for submitting your review!"})
            else:
                return render(request, 'submit_review.html', {'form': form, 'errors': form.errors, 'phone_number': phone_number})
    else:
        # Initial GET request displays the phone number entry form
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
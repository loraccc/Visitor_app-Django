from .models import Review

from .forms import *

import qrcode
import csv

from PIL import Image

from io import BytesIO

from django.db import IntegrityError
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect,get_list_or_404
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
            print(f"Username: {user.username}")
            print(f"Password: {request.POST.get('password1')}")
        
            login(request, user)
            return redirect('/')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    # redirect_authenticated_user = True  
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        """If the form is valid, redirect to the success URL."""
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(f"Valid login attempt with username: {username} and password: {password}")
        messages.success(self.request, "You have successfully logged in.")  # Add a success message
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        print(f"Invalid login attempt with username: {username} and password: {password}")
        messages.error(self.request, "Invalid username or password.")  # Add an error message
        return self.render_to_response(self.get_context_data(form=form))


def home(request):
    return render(request, 'home.html') 


def submit_review(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', None)
        
        if not phone_number:
            # If phone number is not provided, render the phone number form
            form = PhoneNumberForm()
            return render(request, 'phone_number.html', {'form': form})

        # Check if the phone number already exists
        existing_reviews = Review.objects.filter(phone_number=phone_number)
        
        if existing_reviews.exists():
            # Redirect to the simple review form for updating/adding a new review
            return redirect('simple-review', phone_number=phone_number)
        else:
            # Collect full info if no review exists
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
def simple_review(request, phone_number):
    existing_reviews = get_list_or_404(Review, phone_number=phone_number)
    
    if request.method == 'POST':
        form = SimpleReviewForm(request.POST)
        if form.is_valid():
            try:
                # Create a new review instance with the same phone number
                new_review = form.save(commit=False)
                new_review.phone_number = phone_number  # Keep the same phone number
                new_review.pk = None  # Ensure a new instance is created
                new_review.save()
                return redirect('home')  # Redirect to a success page or your desired URL
            except IntegrityError:
                form.add_error(None, "A review with this phone number already exists.")
        
    else:
        # Initialize the form with existing review data (use data from the first review)
        first_review = existing_reviews[0]
        form = SimpleReviewForm(initial={
            'name': first_review.name,
            'phone_number': first_review.phone_number,
            'email': first_review.email,
            'department': first_review.department,
            'purpose': first_review.purpose,
            'other_purpose': first_review.other_purpose,
            'review': first_review.review,
        })
    
    return render(request, 'simple_review.html', {'form': form, 'existing_reviews': existing_reviews})

def review_qr(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'review_qr.html', {'review': review})

def see_qr(request):

    return render(request, 'qr.html')



def visitor_statistics(request):
    today = timezone.now().date()
    
    # Today's data
    total_visitors_today = Review.objects.filter(created_at__date=today).count()
    reviews_today = Review.objects.filter(created_at__date=today)
    
    # All-time data
    total_visitors_all_time = Review.objects.count()
    all_reviews = Review.objects.all()
    
    # Department and purpose choices
    departments = [choice[1] for choice in Review.DEPARTMENT_CHOICES]
    purposes = [choice[1] for choice in Review.PURPOSE_CHOICES]
    
    return render(request, 'visitor_statistics.html', {
        'total_visitors_today': total_visitors_today,
        'reviews_today': reviews_today,
        'total_visitors_all_time': total_visitors_all_time,
        'all_reviews': all_reviews,
        'departments': departments,
        'purposes': purposes,
    })


def export_visitor_statistics_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitor_statistics.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone Number', 'Department', 'Purpose', 'Review', 'Created At'])

    reviews = Review.objects.all()
    for review in reviews:
        writer.writerow([
            review.name,
            review.email,
            review.phone_number,
            review.get_department_display(),
            review.get_purpose_display(),
            review.review,
            review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return response
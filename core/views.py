from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, StreamingHttpResponse
from django.db import IntegrityError

from .models import Review
from .forms import CustomUserCreationForm, PhoneNumberForm, FullReviewForm, SimpleReviewForm
import csv
from io import BytesIO

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('see_qr')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def submit_review(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', None)
        
        if not phone_number:
            form = PhoneNumberForm()
            return render(request, 'phone_number.html', {'form': form})

        existing_reviews = Review.objects.filter(phone_number=phone_number)
        
        if existing_reviews.exists():
            return redirect('simple-review', phone_number=phone_number)
        else:
            form = FullReviewForm(request.POST)
            if form.is_valid():
                Review.objects.create(
                    name=form.cleaned_data['name'],
                    phone_number=form.cleaned_data['phone_number'],
                    email=form.cleaned_data['email'],
                    review=form.cleaned_data['review']
                )
                return HttpResponse("Thank you for submitting your review!")
            else:
                return render(request, 'submit_review.html', {'form': form, 'phone_number': phone_number})
    else:
        form = PhoneNumberForm()
        return render(request, 'phone_number.html', {'form': form})

def simple_review(request, phone_number):
    existing_reviews = get_list_or_404(Review, phone_number=phone_number)
    
    if request.method == 'POST':
        form = SimpleReviewForm(request.POST)
        if form.is_valid():
            try:
                new_review = form.save(commit=False)
                new_review.phone_number = phone_number
                new_review.pk = None
                new_review.save()
                return redirect('home')
            except IntegrityError:
                form.add_error(None, "A review with this phone number already exists.")
        
    else:
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
    
    total_visitors_today = Review.objects.filter(created_at__date=today).count()
    total_visitors_all_time = Review.objects.count()
    
    departments = [choice[1] for choice in Review.DEPARTMENT_CHOICES]
    purposes = [choice[1] for choice in Review.PURPOSE_CHOICES]
    
    return render(request, 'visitor_statistics.html', {
        'total_visitors_today': total_visitors_today,
        'total_visitors_all_time': total_visitors_all_time,
        'departments': departments,
        'purposes': purposes,
    })

def export_visitor_statistics_csv(request):
    def generate():
        writer = csv.writer(BytesIO())
        writer.writerow(['Name', 'Email', 'Phone Number', 'Department', 'Purpose', 'Review', 'Created At'])
        
        for review in Review.objects.all():
            writer.writerow([
                review.name,
                review.email,
                review.phone_number,
                review.get_department_display(),
                review.get_purpose_display(),
                review.review,
                review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])
        return writer.getvalue()
    
    response = StreamingHttpResponse(generate(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitor_statistics.csv"'
    return response

def dashboard_view(request):
    return render(request, 'pages/index.html')

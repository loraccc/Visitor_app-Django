from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NumberForm, UserForm, ReviewForm
from . models import User_number

def Number_Form(request):
    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            if User_number.objects.filter(mobile_number=mobile_number).exists():
                return redirect('review1')
            form.save()
            return redirect('review')  # Redirect to Review_Form
    else:
        form = NumberForm()

    return render(request, 'number_form.html', {'form': form})

def Review_Form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for your review')
    else:
        form = UserForm()
    
    # Ensure that an HttpResponse is returned in all cases
    return render(request, 'review_form.html', {'form': form})

def Review1_Form(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for your review')
    else:
        form = ReviewForm()
    
    # Ensure that an HttpResponse is returned in all cases
    return render(request,'review1_form.html', {'form': form})


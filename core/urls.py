from django.urls import path
from django import views
from .views import register, CustomLoginView,home,submit_review,review_qr,see_qr,visitor_statistics, simple_review
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Redirect to login after logout
    path('home', home, name='home'),  # Add your home view here
    path('submit-review/', submit_review, name='submit-review'),
    path('simple-review/<str:phone_number>/', simple_review, name='simple-review'),
    path('review-qr/<int:pk>/', review_qr, name='review_qr'),
    path('visitor_statistics', visitor_statistics, name='visitor_statistics'),
    path('', see_qr, name='see_qr'),
]
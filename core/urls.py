from django.urls import path
from django import views
from django.contrib.auth.views import LogoutView

from .views import (register, CustomLoginView,home,
                    submit_review,review_qr,
                    see_qr,
                    visitor_statistics,export_visitor_statistics_csv)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Redirect to login after logout


    path('home', home, name='home'),  # Add your home view here


    path('submit-review/', submit_review, name='submit-review'),
    path('review-qr/<int:pk>/', review_qr, name='review_qr'),


    path('visitor_statistics', visitor_statistics, name='visitor_statistics'),
    path('visitor_statistics/csv/', export_visitor_statistics_csv, name='export_visitor_statistics_csv'),

    path('', see_qr, name='see_qr'),
]
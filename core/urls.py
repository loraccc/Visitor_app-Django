from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (register, custom_login, home,
                    submit_review, review_qr, simple_review,
                    see_qr, dashboard_view,
                    visitor_statistics, export_visitor_statistics_csv)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', home, name='home'),
    path('submit-review/', submit_review, name='submit-review'),
    path('simple-review/<str:phone_number>/', simple_review, name='simple-review'),
    path('review-qr/<int:pk>/', review_qr, name='review_qr'),
    path('visitor_statistics/', visitor_statistics, name='visitor_statistics'),
    path('visitor_statistics/csv/', export_visitor_statistics_csv, name='export_visitor_statistics_csv'),
    path('qr/', see_qr, name='see_qr'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

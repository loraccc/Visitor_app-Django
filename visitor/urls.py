from django.urls import path
from . qr_generator import generate_qr_code
from . views import Number_Form, Review_Form, Review1_Form


urlpatterns = [
    path('', generate_qr_code , name='qr_image'),
    path('number_form/',Number_Form,  name='number'),
    path('review_form/', Review_Form, name= 'review'),
    path('review1_form/', Review1_Form, name= 'review1'),
]

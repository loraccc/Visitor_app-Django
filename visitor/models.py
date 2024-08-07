from django.db import models


class User_number(models.Model):
    mobile_number = models.CharField(max_length=16, blank= False, null= False)

    def __str__(self):
        return self.mobile_number

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    review = models.TextField()

    def __str__(self):
        return self.username

class Review_page(models.Model):
    review = models.TextField()

    def __str__(self):
        return self.review



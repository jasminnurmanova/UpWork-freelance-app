from django.contrib.auth.models import AbstractUser
from django.db import models
from service.models import Project
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="users/avatar/", blank=True, null=True)

    def __str__(self):
        return self.username

class Bid(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),)

    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="bids")
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    status = models.CharField( max_length=20,choices=STATUS_CHOICES,default='pending' )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'freelancer']
    def __str__(self):
        return f"{self.freelancer} - {self.project}"


class Contract(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'), )

    project = models.OneToOneField(Project,on_delete=models.CASCADE,related_name="contract")
    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="client_contracts")
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="freelancer_contracts")
    agreed_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    finished_at = models.DateTimeField( null=True,blank=True)

    def __str__(self):
        return f"Contract - {self.project.title}"

class Review(models.Model):
    contract = models.OneToOneField(Contract,on_delete=models.CASCADE, related_name="review" )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review for {self.contract.project.title}"


class Submission(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="submissions")
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="project_submissions/")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
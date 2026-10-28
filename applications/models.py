
from django.conf import settings
from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        null=True,
        blank=True
    )

    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=50, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_on = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    job_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.company} - {self.role}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100, default="Your Name")
    headline = models.CharField(max_length=160, blank=True)
    email = models.EmailField(blank=True)
    university = models.CharField(max_length=160, blank=True)
    degree = models.CharField(max_length=160, blank=True)
    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    target_role = models.CharField(max_length=100, blank=True)
    skills = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    about = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

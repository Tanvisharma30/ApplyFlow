
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Application, UserProfile

User = get_user_model()


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'company',
            'role',
            'location',
            'job_type',
            'status',
            'deadline',
            'job_link',
            'notes',
        ]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'name',
            'headline',
            'email',
            'university',
            'degree',
            'graduation_year',
            'target_role',
            'skills',
            'location',
            'linkedin_url',
            'github_url',
            'about',
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
            'graduation_year': forms.NumberInput(
                attrs={'min': 2000, 'max': 2100}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

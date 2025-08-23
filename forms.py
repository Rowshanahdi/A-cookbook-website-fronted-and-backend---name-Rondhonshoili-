from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user















from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    COUNTRY_CHOICES = [
        ('Bangladesh', 'Bangladesh'),
        ('India', 'India'),
        ('USA', 'USA'),
        ('Other', 'Other'),
    ]

    ENQUIRY_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Enquiry', 'Enquiry'),
        ('Feedback', 'Feedback'),
        ('Other', 'Other'),
    ]

    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    enquiry_for = forms.ChoiceField(choices=ENQUIRY_CHOICES)

    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'country', 'enquiry_for', 'subject', 'message']






























from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'name', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name'})
        }
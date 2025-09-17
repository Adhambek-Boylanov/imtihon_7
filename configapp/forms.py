from django import forms
from .models import *
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "technologies", "tech_stack", "repo_link"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter project title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter project description"
            }),
            "technologies": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Django • REST • Docker"
            }),
            "tech_stack": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Django, PostgreSQL, Bootstrap"
            }),
            "repo_link": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://github.com/username/repo"
            }),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'style': 'padding:10px; border-radius:6px; width:100%'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'style': 'padding:10px; border-radius:6px; width:100%'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'style': 'padding:10px; border-radius:6px; width:100%; min-height:120px; resize:vertical;'}),
        }



class UserLoginForm(forms.Form):
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    password = forms.CharField(label='parol', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}))

    class Meta:
        fields = ['username', 'password']
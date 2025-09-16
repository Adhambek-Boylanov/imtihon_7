from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import PersonalInfo, Skill, Education, Experience, Project
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor



@login_required(login_url='login')
def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFillColor(HexColor("#0f1724"))
    p.rect(0, 0, width, height, fill=1)

    y = height - 50

    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(HexColor("#6EE7B7"))
    p.drawString(40, y, "Hi, I'm Adhambek")
    y -= 30

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#cfeef4"))
    p.drawString(40, y, "I build fast, accessible and delightful web applications using Django, Python and modern UI patterns.")
    y -= 40

    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Skills:")
    y -= 20

    skills = ["Django", "REST API", "PostgreSQL", "HTML", "Celery"]
    x = 40
    for skill in skills:
        p.setFont("Helvetica", 12)
        p.setFillColor(HexColor("#e6eef8"))
        p.drawString(x, y, f"- {skill}")
        y -= 15

    y -= 10
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Experience:")
    y -= 20

    experiences = [
        ("2025 — Present", "Backend Developer — Acme Tech: Working on APIs, payment integrations, and microservice orchestration."),
        ("2024 — 2025", "Backend Developer — Freelance: Delivered several Django applications for small businesses."),
        ("2024 — 2025", "Junior Developer — Startup: Helped build core features and CI/CD pipelines.")
    ]

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for time, desc in experiences:
        p.drawString(50, y, f"{time} | {desc}")
        y -= 25

    y -= 10
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Education:")
    y -= 20

    educations = [
        ("2024— 2025", "Python-Django Backend — Najot Talim"),
        ("2024 — 2025", "High School Diploma — Focus on mathematics and informatics")
    ]

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for time, desc in educations:
        p.drawString(50, y, f"{time} | {desc}")
        y -= 20

    y -= 10
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Portfolio Projects:")
    y -= 20

    projects = [
        ("Taxi Park System", "Django-based dispatch system with driver ratings, fare calculation, trip management."),
        ("Shoply — E-commerce", "Online store with cart, checkout, payment integrations, and order tracking."),
        ("Personal Portfolio", "Static and dynamic portfolio with contact form and CMS backend."),
        ("ToDo App", "Task manager with reminders and tagging features."),
        ("Headless Blog CMS", "API-first blog with markdown editor and RSS feeds."),
        ("Gallery App", "Fast image serving with lazy-loading and lightbox experience.")
    ]

    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#e6eef8"))
    for title, desc in projects:
        p.drawString(50, y, f"- {title}: {desc}")
        y -= 20
        if y < 100:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="cv.pdf")


@login_required(login_url='login')
def index(request):
    personalinfo = PersonalInfo.objects.first()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    projects = Project.objects.all()
    context = {
        'personalinfo': personalinfo,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'projects': projects
    }
    return render(request, 'index1.html',context=context)


@login_required(login_url='login')
def contact_message(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent!")
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


def login_views(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Xush kelibsiz, " + username + "!")
                return redirect("index")
            else:
                messages.error(request, "Login yoki parol xato!")
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect("login")

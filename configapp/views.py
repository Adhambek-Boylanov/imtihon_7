from django.shortcuts import render, redirect, get_object_or_404
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
from django.http import HttpResponse


def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFillColor(HexColor("#0f1724"))
    p.rect(0, 0, width, height, fill=1)

    y = height - 50
    personal = PersonalInfo.objects.first()
    if personal:
        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(HexColor("#6EE7B7"))
        p.drawString(40, y, f"Hi, I'm {personal.name}")
        y -= 30

        p.setFont("Helvetica", 14)
        p.setFillColor(HexColor("#cfeef4"))
        p.drawString(40, y, personal.profession)
        y -= 25

        p.setFont("Helvetica", 12)
        p.setFillColor(HexColor("#cfeef4"))
        p.drawString(40, y, personal.about[:100])
        y -= 40

    skills = Skill.objects.all()
    if skills.exists():
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(HexColor("#60A5FA"))
        p.drawString(40, y, "Skills:")
        y -= 20

        for skill in skills:
            p.setFont("Helvetica", 12)
            p.setFillColor(HexColor("#e6eef8"))
            p.drawString(50, y, f"- {skill.name} ({skill.level})")
            y -= 15

    experiences = Experience.objects.all().order_by("-start_date")
    if experiences.exists():
        y -= 20
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(HexColor("#60A5FA"))
        p.drawString(40, y, "Experience:")
        y -= 20

        for exp in experiences:
            end = exp.end_date.strftime("%Y-%m") if exp.end_date else "Present"
            time = f"{exp.start_date.strftime('%Y-%m')} — {end}"
            text = f"{time} | {exp.position} @ {exp.company_name}"
            p.setFont("Helvetica", 12)
            p.setFillColor(HexColor("#e6eef8"))
            p.drawString(50, y, text)
            y -= 15

            for line in exp.description.split("\n"):
                p.drawString(60, y, f"- {line}")
                y -= 15
            y -= 10

    educations = Education.objects.all().order_by("-start_date")
    if educations.exists():
        y -= 20
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(HexColor("#60A5FA"))
        p.drawString(40, y, "Education:")
        y -= 20

        for edu in educations:
            end = edu.end_date.strftime("%Y-%m") if edu.end_date else "Present"
            time = f"{edu.start_date.strftime('%Y-%m')} — {end}"
            text = f"{time} | {edu.institution} ({edu.degree})"
            p.setFont("Helvetica", 12)
            p.setFillColor(HexColor("#e6eef8"))
            p.drawString(50, y, text)
            y -= 15

            if edu.description:
                p.drawString(60, y, f"- {edu.description}")
                y -= 15
            y -= 5

    projects = Project.objects.all()
    if projects.exists():
        y -= 20
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(HexColor("#60A5FA"))
        p.drawString(40, y, "Portfolio Projects:")
        y -= 20

        for proj in projects:
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(HexColor("#e6eef8"))
            p.drawString(50, y, f"- {proj.title}")
            y -= 15

            p.setFont("Helvetica", 11)
            p.drawString(60, y, proj.description[:90])  # uzun bo‘lsa kesamiz
            y -= 15

            p.setFont("Helvetica-Oblique", 10)
            p.drawString(60, y, f"Tech: {proj.tech_stack}")
            y -= 15

            if proj.repo_link:
                p.setFont("Helvetica-Oblique", 10)
                p.drawString(60, y, f"Repo: {proj.repo_link}")
                y -= 15

            y -= 10
            if y < 100:
                p.showPage()
                y = height - 50

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="cv.pdf")

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
                return redirect("admin")
            else:
                messages.error(request, "Login yoki parol xato!")
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect("index")

@login_required(login_url='login')
def admin(request):
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
    return render(request, 'admin.html',context=context)


@login_required(login_url='login')
def edit_profile(request):
    user = PersonalInfo.objects.all().first()
    if request.method == "POST":
        form = PersonalInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("admin")
    else:
        form = PersonalInfoForm(instance=user)

    return render(request, "edit_profile.html", {"form": form})


@login_required(login_url='login')
def add_projects(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = ProjectForm()
    return render(request, 'add_projects.html', {'form': form})

@login_required(login_url='login')
def message_list(request):
    messages = ContactMessage.objects.all().order_by("-created_at")
    return render(request, "messages.html", {"messages": messages})

@login_required(login_url='login')
def projects_list(request):
    project = Project.objects.all()
    return render(request,'projects.html',{'projects':project})

@login_required(login_url='login')
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects_list")
    return render(request, "delete_confirm.html", {"project": project})



from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    tech_stack = models.CharField(max_length=255)  # masalan: "Django, PostgreSQL, Bootstrap"
    repo_link = models.URLField(blank=True, null=True)

    def get_tech_list(self):
        return [t.strip() for t in self.technologies.split("•")]

class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    about = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    image = models.ImageField(upload_to='personal_images/', blank=True, null=True)

    def __str__(self):
        return self.name
class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Experience(models.Model):
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.position} - {self.company_name}"

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.institution

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
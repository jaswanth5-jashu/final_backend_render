from django.db import models

class CareerApplication(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=150)
    cgpa = models.CharField(max_length=10)
    year_of_passing = models.IntegerField()
    experience = models.CharField(max_length=50, blank=True)
    skills = models.TextField()
    resume = models.FileField(upload_to='resume/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
   
def mou_upload_path(instance, filename):
    return f"mous/{instance.category}/{filename}"

class MOU(models.Model):

    CATEGORY_CHOICES = [
        ("cloud", "Cloud"),
        ("education", "Education"),
        ("security", "Security"),
        ("innovation", "Innovation"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    highlights = models.JSONField(help_text="Example: ['Point 1', 'Point 2']")
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class")
    start_date = models.DateField()

    pdf = models.FileField(upload_to=mou_upload_path)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

#gallery

def gallery_upload_path(instance, filename):
    # media/gallery/Events/filename.jpg
    return f"gallery/{instance.category}/{filename}"

def gallery_upload_path(instance, filename):
    # media/gallery/Events/filename.jpg
    return f"gallery/{instance.category}/{filename}"

class GalleryImage(models.Model):

    CATEGORY_CHOICES = [
        ('Events', 'Events'),
        ('Activities', 'Activities'),
        ('Achievements', 'Achievements'),
        ('Office', 'Office'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to=gallery_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"
    
class Project(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
    )

    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming"
    )
    progress = models.PositiveIntegerField(default=0)  # only for active
    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class CommunityItem(models.Model):

    SECTION_CHOICES = (
        ('giveback', 'Give Back'),
        ('general', 'General'),
    )

    ITEM_TYPE_CHOICES = (
        ('gallery', 'Gallery'),
        ('workshop', 'Workshop'),
    )

    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('upcoming', 'Upcoming'),
    )

    section = models.CharField(
        max_length=20,
        choices=SECTION_CHOICES,
        default='general'
    )

    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Workshop only
    date = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    participants = models.PositiveIntegerField(null=True, blank=True)

    # Gallery only
    image = models.ImageField(upload_to="give-gallery/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.section} | {self.item_type} | {self.title}"
    


class CpuInquiry(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    cpu_model = models.CharField(max_length=100)
    quantity = models.IntegerField()
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

from django.db import models


class HackathonTeam(models.Model):
    team_name = models.CharField(max_length=150)
    total_participants = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name


class HackathonParticipant(models.Model):
    ROLE_CHOICES = (
        ("LEADER", "Leader"),
        ("MEMBER", "Member"),
    )

    team = models.ForeignKey(
        HackathonTeam,
        on_delete=models.CASCADE,
        related_name="participants"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    branch = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    year = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

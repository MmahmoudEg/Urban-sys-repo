from django.db import models


# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lawyer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)   # Furniture, Lighting, Paint...
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Case(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('OPEN', 'Open'),
        ('CLOSED', 'CLOSED')
    )
    COURT_CHOICES = (
        ('New cairo', 'New cairo'),
        ('Zayed', 'Zayed'),
        ('Nasr city', 'Nasr city'),
        ('New admin capital', 'New admin capital'),
        ('ay ebn mtnaka', 'ay ebn mtnaka'),
    )
    CASE_TYPE_CHOICES = (
        ('Interior design', 'Interior design'),
        ('3d design only', '3d design only'),
        ('CIVIL', 'CIVIL'),
        ('ADMIN', 'ADMIN'),
    )

    case_number = models.CharField(max_length=20, unique=True, blank=False, null=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    court = models.CharField(max_length=20, choices=COURT_CHOICES, default='CAIRO_COURT')
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, default='Legal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
# Add Document model

class Document(models.Model):
    case = models.ForeignKey(
        Case, 
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/", null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
# Add to models.py after Document model
class Hearing(models.Model):
    case = models.ForeignKey(
        Case, 
        on_delete=models.CASCADE,
        related_name='hearings'
    )
    hearing_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['hearing_date']
        
    def __str__(self):
        return f"Hearing on {self.hearing_date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['hearing_date']
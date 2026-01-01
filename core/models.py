from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Model(models.Model):
    TYPE_CHOICES = [
        ('chatgpt', 'ChatGPT'),
        ('ollama', 'Ollama'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    apikey = models.CharField(max_length=255, blank=True)
    paikey = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    cant = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    importe = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # Calculate importe automatically - ensure values are Decimal
        self.cant = Decimal(str(self.cant)) if self.cant else Decimal('0')
        self.price = Decimal(str(self.price)) if self.price else Decimal('0')
        self.importe = self.cant * self.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.cant} @ {self.price}"


class Agent(models.Model):
    PERIODICITY_CHOICES = [
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
    ]
    
    name = models.CharField(max_length=100)
    descripcion = models.TextField()
    ai_model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='agents')
    prompt = models.TextField()
    is_active = models.BooleanField(default=True)
    periodicity_value = models.IntegerField(default=5)
    periodicity_unit = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, default='minutes')
    start_time = models.TimeField(default='08:00')
    end_time = models.TimeField(default='20:00')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_periodicity_display_text(self):
        return f"Every {self.periodicity_value} {self.get_periodicity_unit_display().lower()}"


class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('working', 'Working'),
        ('completed', 'Completed'),
    ]
    
    sequence = models.CharField(max_length=20, unique=True, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='work_orders')
    prompt = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_time = models.TimeField(default='08:00')
    end_time = models.TimeField(default='20:00')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.sequence:
            # Generate sequence number OT-000001
            last_order = WorkOrder.objects.order_by('-id').first()
            if last_order and last_order.sequence:
                last_number = int(last_order.sequence.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.sequence = f"OT-{new_number:06d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sequence} - {self.agent.name}"

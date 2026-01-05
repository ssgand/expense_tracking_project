from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserCategoryRelationship(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, preferred_currency, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not preferred_currency:
            raise ValueError('Users must have a preferred currency')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, preferred_currency=preferred_currency, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, preferred_currency='USD', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, preferred_currency, password, **extra_fields)

class CustomUser(TimestampedModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True, blank=False, null=False)
    preferred_currency = models.CharField(max_length=3, blank=False, null=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['preferred_currency']

class Categories(TimestampedModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

class Expenses(TimestampedModel, UserCategoryRelationship):
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    currency = models.CharField(max_length=3)
    description = models.TextField(blank=True, null=True)
    expense_date = models.DateField()

class Frequency(models.TextChoices):
    DAILY = 'DAILY', 'Daily'
    WEEKLY = 'WEEKLY', 'Weekly'
    MONTHLY = 'MONTHLY', 'Monthly'
    YEARLY = 'YEARLY', 'Yearly'

class RecurringExpenses(TimestampedModel, UserCategoryRelationship):
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3)
    next_pay_date = models.DateField()
    frequency = models.CharField(max_length=50, choices=Frequency.choices, default=Frequency.MONTHLY)

class Budgets(TimestampedModel, UserCategoryRelationship):
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    currency = models.CharField(max_length=3)
    start_date = models.DateField()
    end_date = models.DateField()


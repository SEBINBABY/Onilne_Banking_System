from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class AccountDB(models.Model):
    ACCNAME = models.CharField(max_length=100, null=True, blank=True)
    ACCDESC = models.CharField(max_length=100, null=True, blank=True)
    ACCFULLDESC = models.CharField(max_length=2500, null=True, blank=True)
    ACCIMAGE = models.ImageField(upload_to='Images', null=True, blank=True)

class AccountTypeDB(models.Model):
    ACCOUNT = models.CharField(max_length=100, null=True, blank=True)
    ACCOUNTTYPE = models.CharField(max_length=100, null=True, blank=True)
    SHORTDESC = models.CharField(max_length=800, null=True, blank=True)
    FULLDESC = models.CharField(max_length=3000, null=True, blank=True)
    TYPEIMAGE = models.ImageField(upload_to='Images', null=True, blank=True)

class LoanDb(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=800, null=True, blank=True)
    image = models.ImageField(upload_to='Images', null=True, blank=True)

class BankNews(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    short_description = models.CharField(max_length=2000, null=True, blank=True)
    full_description = models.CharField(max_length=3000, null=True, blank=True)
    news_image = models.ImageField(upload_to='Images', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

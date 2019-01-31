from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Location(models.Model):
    """
    Represents a physical location where the user is located
    """
    name = models.CharField(max_length=256)
    address = models.ForeignKey("StreetAddress", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class StreetAddress(models.Model):
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.address_1}, {self.city}"

class CoreUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates a basic user that just needs the email
        """
        if not email:
            raise ValueError("User must have an email address")

        user_prefs = UserPreferences()
        user_prefs.save()

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            preferences=user_prefs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates a super user that just needs email
        """
        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserPreferences(models.Model):
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)
    timezone = models.CharField(max_length=64, blank=True, null=True)


class CoreUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    preferences = models.OneToOneField(UserPreferences, on_delete=models.CASCADE)

    objects = CoreUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin


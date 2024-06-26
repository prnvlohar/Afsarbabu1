

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from users.managers import CustomUserManager


class CustomUser(AbstractUser):

    TYPE = (
        ('student', 'Student'),
        ('institute', 'Institute'),
        ('instructor', 'Instructor'),
    )

    username = None

    phone = models.CharField(unique=True, null=True, max_length=12)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255,
                                validators=[
                                    MinLengthValidator(limit_value=8,
                                                       message='Password must be atleast 8 characters long.'),
                                    RegexValidator(regex=r'[A-Za-z]',
                                                   message='Password must contain one Upper and lower character.'),
                                    RegexValidator(regex=r'[0-9]',
                                                   message='Password must contain atleast one digit.'),
                                    RegexValidator(regex=r'[!@#$%&*]',
                                                   message='Password must contain atleast one special char.'),
                                ])
    type = models.CharField(max_length=100,
                            choices=TYPE, default='student')
    institute = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    referral_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    recommended_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recommended_users'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def clean(self):
        super().clean()
        self.validate_password_complexity()

    def validate_password_complexity(self):
        if not any(char.isdigit() for char in self.password):
            raise ValidationError("password must contain atleast one digit")

    def __str__(self):
        return self.email

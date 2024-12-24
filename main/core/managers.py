from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a regular user with a username and password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with a username, password, and the 'admin' role.
        """
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)  # Ensure the user is staff
        extra_fields.setdefault('is_superuser', True)  # Ensure the user is superuser
        
        return self.create_user(username, password, **extra_fields)

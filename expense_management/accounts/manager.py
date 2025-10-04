from django.contrib.auth.models import BaseUserManager

# Custom Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role=None, company=None):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, company=company)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password, role='company_admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

from django.contrib.auth.models import UserManager as DjangoUserManager


class CustomUserManager(DjangoUserManager):
    def create(self, email, password=None, **kwargs):
        kwargs['username'] = email
        user = super().create(email=email, **kwargs)
        if password is not None:
            user.set_password(password)
            user.save()
        return user

    def create_user(self, email, **kwargs):
        kwargs.update(
            is_staff=False,
            is_superuser=False,
        )
        return self.create(email, **kwargs)

    def create_staff(self, email, **kwargs):
        kwargs.update(
            is_staff=True,
            is_superuser=False,
        )
        return self.create(email, **kwargs)
    
    def create_superuser(self, email, **kwargs):
        kwargs.update(email=email, is_staff=True, username=email)
        kwargs.setdefault('is_active', True)
        return super().create_superuser(**kwargs)

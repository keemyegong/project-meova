from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from allauth.account.adapter import DefaultAccountAdapter

def username(user, file):
    string_username = str(user).split()[0]
    return f"profiles/{string_username}/{file}"

class User(AbstractUser):
    nickname=models.CharField(max_length=100)
    followings=models.ManyToManyField('self',related_name='followers',symmetrical=False)
    bio=models.TextField()
    profile_photo=models.ImageField(blank=True,upload_to=username)
    
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # Saves a new `User` instance using information provided in the
        # signup form.
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # nickname 필드를 추가
        nickname = data.get("nickname")
        followings=data.get('followings')
        bio=data.get('bio')
        profile_photo=data.get('profile_photo')
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if bio:
            user_field(user, "bio", bio)
        if profile_photo:
            user_field(user, "profile_photo", profile_photo)
        if followings:
            user_field(user, "followings", followings)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user
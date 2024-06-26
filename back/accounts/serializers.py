from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from movies.serializers import MovieListSerializer, ReviewSerializer
UserModel = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
  # 필요한 필드들을 추가합니다.
  nickname = serializers.CharField(
  required=False,
  allow_blank=True,
  max_length=255
  )
  
  # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
  def get_cleaned_data(self):
    return {
    'username': self.validated_data.get('username', ''),
    'password1': self.validated_data.get('password1', ''),
    # nickname 필드 추가
    'nickname': self.validated_data.get('nickname', ''),
    'bio': self.validated_data.get('bio', ''),
    'profile_photo': self.validated_data.get('profile_photo', ''),
    'email': self.validated_data.get('email', ''),
    }

# 상세정보 페이지용 serializer
class CustomUserDetailsSerializer(UserDetailsSerializer):
  followers = serializers.SerializerMethodField()
  class Meta:
    extra_fields = []
    # see https://github.com/iMerica/dj-rest-auth/issues/181
    # UserModel.XYZ causing attribute error while importing other
    # classes from `serializers.py`. So, we need to check whether the auth model has
    # the attribute or not
    if hasattr(UserModel, 'USERNAME_FIELD'):
      extra_fields.append(UserModel.USERNAME_FIELD)
    if hasattr(UserModel, 'EMAIL_FIELD'):
      extra_fields.append(UserModel.EMAIL_FIELD)
    if hasattr(UserModel, 'first_name'):
      extra_fields.append('first_name')
    if hasattr(UserModel, 'last_name'):
      extra_fields.append('last_name')
    if hasattr(UserModel, 'nickname'):
      extra_fields.append('nickname') 
    if hasattr(UserModel, 'bio'):
      extra_fields.append('bio') 
    if hasattr(UserModel, 'profile_photo'):
      extra_fields.append('profile_photo') 
    if hasattr(UserModel, 'followings'):
      extra_fields.append('followings') 
    model = UserModel
    fields = ('pk','followers', *extra_fields)
    read_only_fields = ('email',)
  def get_followers(self, obj):
        # Get all follower objects
        followers = obj.followers.all()
        # Extract and return only the primary keys
        print(followers)
        return [follower.pk for follower in followers]
# class UserPkSerializer(serializers.ModelSerializer):
#   class Meta:
#     model=UserModel
#     fields=('pk',)
class ProfileSerializer(serializers.ModelSerializer):
  followers = serializers.SerializerMethodField()
  liked_movies = MovieListSerializer(many=True, read_only=True)
  liked_reviews = ReviewSerializer(many=True, read_only=True)
  
  class Meta:
      model = UserModel
      fields = ('pk', 'username', 'email', 'bio', 'nickname', 'profile_photo', 'followings','followers', 'liked_movies', 'liked_reviews',)

  def get_followers(self, obj):
        # Get all follower objects
        followers = obj.followers.all()
        # Extract and return only the primary keys
        return [follower.pk for follower in followers]
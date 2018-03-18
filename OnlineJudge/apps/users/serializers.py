from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserChangePasswordSerializer(serializers.ModelSerializer):
    #这里可以对字段进行限制，只要保证名字跟数据库中的字段名相同即可
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User  #所使用的数据库
        fields = ('username','password')  #所选用的字段
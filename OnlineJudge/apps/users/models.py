from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


#用户类型
class AdminType(object):
    USER = "User"
    ADMIN = "Admin"
    SUPER_ADMIN = "Super Admin"

#问题的权限
class ProblemPermission(object):
    NONE = "None"
    OWN = "Own"
    ALL = "All"


class UserProfile(AbstractUser):  #AbstractBaseUser可以自定义认证模式
    '''
    用户
    '''
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=64, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    # One of UserType
    admin_type = models.CharField(max_length=32, default=AdminType.USER)
    problem_permission = models.CharField(max_length=32, default=ProblemPermission.NONE)
    reset_password_token = models.CharField(max_length=32, null=True)  #重置密码令牌
    reset_password_token_expire_time = models.DateTimeField(null=True)  #重置密码令牌过期时间

    '''
    # SSO auth token
    auth_token = models.CharField(max_length=32, null=True)
    two_factor_auth = models.BooleanField(default=False)
    tfa_token = models.CharField(max_length=32, null=True)
    session_keys = JSONField(default=list)
    '''
    '''
    # open api key
    open_api = models.BooleanField(default=False)
    open_api_appkey = models.CharField(max_length=32, null=True)
    is_disabled = models.BooleanField(default=False)
    '''

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


'''
class VerifyCode(models.Model):
    
    code = models.CharField(max_length=10,verbose_name="验证码")
    mobile = models.CharField(max_length=11,verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta():
        verbose_name = "验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
'''
"""OnlineJudge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers


from users.views import UsersViewSet,UserChangePasswordViewSet
from problem.views import ProblemViewSet



router = routers.DefaultRouter()

#配置user的url
router.register(r'user',UsersViewSet,base_name="user") #用户信息注册
router.register(r'changepw',UserChangePasswordViewSet,base_name="changepw")

#配置problem的url
router.register(r'problem',ProblemViewSet,base_name="problem")

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls')),
]

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class ProblemTag(models.Model):
    tag_name = models.CharField(max_length=20)

    class Meta:
        db_table = "problem_tag"

class ProblemDifficulty(object):
    HIGH = "high"
    MID = "Mid"
    LOW = "Low"

class Problem(models.Model):
    """
    oj平台数据库设计
    """
    # id information
    #problem.Problem: (models.E004) 'id' can only be used as a field name if the field also sets 'primary_key=True'.
    _id = models.CharField(max_length=24,db_index=True)  #db_index数据库将创建id为索引

    #contest problem
    is_public = models.BooleanField(default=False)
    title = models.CharField(max_length=128)
    #problem_editor(尚未加入xss过滤器)
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    hint = models.TextField()

    time_limit = models.IntegerField() #ms
    memory_limit = models.IntegerField() #MB
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    create_by = models.ForeignKey(User)
    visible = models.BooleanField(default=True) #visible->题目是否可见
    tags = models.ManyToManyField(ProblemTag)  #多对多数据库模型
    source = models.CharField(max_length=200)
    # 测试样例

    # 测试数据

    # special judge


    submit_number = models.BigIntegerField(default=0)
    accepted_number = models.BigIntegerField(default=0)

    class Meta:
        db_table = "problem"
        unique_together = ("id",)
        #题目排序方式有待改进
        ordering = ("create_time",)


    #这个函数尚未搞懂
    def add_submit_number(self):
        self.submit_number = models.F("submit_number")+1
        self.save(update_fields=["submit_number"])#这句话不懂

    def add_accepted_number(self):
        self.accepted_number = models.F("accepted_number")+1
        self.save(update_fields=["accepted_number"])

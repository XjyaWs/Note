from django.db import models
from user.models import User


# Create your models here.
class Note(models.Model):

    title = models.CharField("标题", max_length=100, default='')
    content = models.TextField("内容")
    # 创建时间
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    # 更新时间
    update_time = models.DateTimeField('更新时间', auto_now=True)

    user = models.ForeignKey(User, related_name='note', on_delete=models.CASCADE)

    # 伪删除字段
    is_active = models.BooleanField("是否被激活", default=True)

    def __str__(self):
        return "标题：{} 作者id：{}".format(self.title, self.user)

    class Meta:

        db_table = "note"

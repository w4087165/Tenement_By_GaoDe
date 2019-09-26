from django.db import models

# Create your models here.
#建立数据库 表结构：
class LianJiaTenementHouse(models.Model):

    house_name = models.CharField(max_length=32,verbose_name='房源名称')

    platform = models.CharField(max_length=6,default='链家网')

    house_message = models.CharField(max_length=64,verbose_name='房源信息')

    price = models.DecimalField(max_digits=8,default='99999', decimal_places=2,verbose_name='租金')  # dicimal(7,2)

    #具体位置 lon：经度， lat：纬度
    lon = models.DecimalField(max_digits=10,decimal_places=6,verbose_name='经度',default=0)

    lat = models.DecimalField(max_digits=10,decimal_places=6,verbose_name='纬度',default=0)

    url = models.CharField(max_length=148,verbose_name='具体链接')

    images = models.CharField(max_length=64,verbose_name='图片')

    class Meta:
        db_table = 'LianJia_table'


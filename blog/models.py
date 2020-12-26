from django.db import models

class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    heading0 = models.CharField(max_length=100)
    content0 = models.CharField(max_length=1000000,default='')
    heading1 = models.CharField(max_length=100)
    content1 = models.CharField(max_length=1000000,default='')
    heading2 = models.CharField(max_length=100)
    content2 = models.CharField(max_length=1000000,default='')
    published = models.DateTimeField()
    author = models.CharField(max_length=100,default='')
    thumbnail = models.ImageField(upload_to='blog/images',default='')

    def __str__(self):
        return self.title
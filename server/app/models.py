from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    img_path = models.ImageField(upload_to='teachers/')
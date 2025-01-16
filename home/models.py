from django.db import models

# Create your models here.
class contactme(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    dsr = models.TextField()
    def __str__(self):
        return self.name + " " + str(self.phone)
    
class user(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    def __str__(self):
        return self.name +'-' + self.email
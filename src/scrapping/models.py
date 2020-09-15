from django.db import models

# Create your models here.
class Make(models.Model):
    make = models.CharField(max_length=40,unique=True)

    def __str__(self):
        return self.make


class Car(models.Model):
    make_id    = models.ForeignKey(Make, on_delete=models.CASCADE, null=True)
    model      = models.CharField(max_length=70,null=True, blank=True)
   
    
    def __str__(self):
        return self.model
    

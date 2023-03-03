from django.db import models
from signup.models import User

# Create your models here.
CATEGORY_CHOICES = (
    ("Mental Health", "Mental Health"),
    ("Heart Disease", "Heart Disease"),
    ("Covid19", "Covid19"),
    ("Immunization", "Immunization"),
)
class Blog(models.Model):
    title = models.CharField(max_length = 50)
    img   = models.ImageField(upload_to='static/blogpics/')
    category = models.CharField(max_length = 50, choices=CATEGORY_CHOICES,default='Mental Health')
    summary = models.CharField(max_length=100)
    content = models.TextField()
    draft = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)

    def __str__(self):
        return self.title

    class Meta:
      db_table = 'blogs'

class Appointment(models.Model):
    speciality = models.CharField(max_length=300,null=False)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='doctors')
    patient = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='patients')
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()

    class Meta:
        db_table = 'appointments'

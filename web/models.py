from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.date}"

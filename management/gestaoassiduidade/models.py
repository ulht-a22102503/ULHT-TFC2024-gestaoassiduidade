from django.db import models


# Create your models here.
#Base de dados no terminal (MariaDB)
class Employee(models.Model):
    id_employee = models.IntegerField(db_column='ID_employee', primary_key=True)
    name = models.CharField(max_length=200, db_column='name')
    
    class Meta:
        managed = False
        db_table = 'employee'

 
class Attendance(models.Model):
    id_attendance = models.IntegerField(db_column='ID_attendance', primary_key=True)
    id_employee = models.ForeignKey(Employee, db_column='ID_employee', on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'attendance'
        

class Fingerprint(models.Model):
    id_fingerprint = models.IntegerField(primary_key=True, db_column='ID_fingerprint')
    id_employee = models.ForeignKey(Employee, db_column='ID_employee', on_delete=models.CASCADE)
    id_sensor_index = models.IntegerField(db_column='ID_sensor_index', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fingerprint'

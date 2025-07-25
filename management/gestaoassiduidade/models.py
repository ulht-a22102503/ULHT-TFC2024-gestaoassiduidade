from django.db import models


# Create your models here.
#Base de dados no terminal (MariaDB)
class JobRole(models.Model):
    id_role = models.CharField(db_column='ID_role', primary_key=True, max_length=4)
    descript = models.CharField(max_length=50)

    def __str__(self):
        return self.descript

    class Meta:
        managed = False
        db_table = 'job_role'


class Shift(models.Model):
    id_shift = models.AutoField(db_column='ID_shift', primary_key=True)
    time_begin = models.TimeField()
    break_begin = models.TimeField(blank=True, null=True)
    break_end = models.TimeField(blank=True, null=True)
    time_end = models.TimeField()

    class Meta:
        managed = False
        db_table = 'shift'


class Workcode(models.Model):
    id_workcode = models.CharField(db_column='ID_workcode', primary_key=True, max_length=4)
    code_type = models.BooleanField()
    descript = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'workcode'


class Employee(models.Model):
    id_employee = models.AutoField(db_column='ID_employee', primary_key=True)
    id_role = models.ForeignKey(JobRole, models.DO_NOTHING, db_column='ID_role')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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


class Credentials(models.Model):
    id_fingerprint = models.AutoField(db_column='ID_fingerprint', primary_key=True)
    id_employee = models.OneToOneField('Employee', models.DO_NOTHING, db_column='ID_employee')
    id_sensor_index_main = models.IntegerField(db_column='ID_sensor_index_main', blank=True, null=True)
    id_sensor_index_sec = models.IntegerField(db_column='ID_sensor_index_sec', blank=True, null=True)
    pincode = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credentials'

class Schedule(models.Model):
    id_schedule = models.AutoField(db_column='ID_schedule', primary_key=True)
    valid_on = models.DateField()
    id_workcode = models.ForeignKey(Workcode, models.DO_NOTHING, db_column='ID_workcode')
    id_shift = models.ForeignKey(Shift, models.DO_NOTHING, db_column='ID_shift', blank=True, null=True)
    id_employee = models.ForeignKey(Employee, models.DO_NOTHING, db_column='ID_employee')

    class Meta:
        managed = False
        db_table = 'schedule'
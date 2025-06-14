from django.db import models


# Create your models here.
#Base de dados no terminal (MariaDB)
class Employee(models.Model):
    id_employee = models.AutoField(db_column='ID_employee', primary_key=True)
    id_role = models.ForeignKey(JobRole, models.DO_NOTHING, db_column='ID_role')
    name = models.CharField(max_length=200)

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


class Credentials(models.Model):
    id_fingerprint = models.AutoField(db_column='ID_fingerprint', primary_key=True)
    id_employee = models.OneToOneField('Employee', models.DO_NOTHING, db_column='ID_employee')
    id_sensor_index_main = models.IntegerField(db_column='ID_sensor_index_main', blank=True, null=True)
    id_sensor_index_sec = models.IntegerField(db_column='ID_sensor_index_sec', blank=True, null=True)
    pincode = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credentials'


class JobRole(models.Model):
    id_role = models.CharField(db_column='ID_role', primary_key=True, max_length=4)
    descript = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'job_role'


class Schedule(models.Model):
    id_schedule = models.AutoField(db_column='ID_schedule', primary_key=True)
    valid_on = models.DateField()
    id_workcode = models.CharField(db_column='ID_workcode', max_length=4)
    id_shift = models.IntegerField(db_column='ID_shift', blank=True, null=True)
    id_employee = models.IntegerField(db_column='ID_employee')

    class Meta:
        managed = False
        db_table = 'schedule'


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
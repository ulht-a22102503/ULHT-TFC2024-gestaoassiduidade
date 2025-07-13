import locale
import calendar
import csv
import io
from datetime import datetime
from gestaoassiduidade.models import Schedule, Workcode, Shift, Employee

locale.setlocale(locale.LC_ALL, 'pt_PT.utf8')

def import_schedule(file, area):
    num_shift = list
    match area:
        case 'ERPI':
            num_shift = [('M',Shift.objects.get(id_shift=1)),('T',Shift.objects.get(id_shift=2)),('N',Shift.objects.get(id_shift=3))]

    sch_vht = Workcode.objects.get(id_workcode='VHT')
    sch_h10 = Workcode.objects.get(id_workcode='H10')
    sch_fds = Workcode.objects.get(id_workcode='FDS')
    sch_fer = Workcode.objects.get(id_workcode='FER')
    sch_flg = Workcode.objects.get(id_workcode='FLG')

    csvfile = file.read().decode('utf-8')
    reader = csv.reader(io.StringIO(csvfile), delimiter=';', quotechar='|')
    schedule_month = next(reader)[8]
    workday = datetime.strptime(schedule_month,'%B %Y')
    offset = 8 + calendar.monthrange(workday.year, workday.month)[1]
    next(reader)
    for row in reader:
        print("ID trabalhador:", row[0], "| Nome trabalhador:", row[1])
        employee = Employee.objects.get(id_employee=row[0])
        employee_schedule = row[8:offset]
        print(employee_schedule,'\n')
        for day, shift in enumerate(employee_schedule, start=1):
            workday = workday.replace(day=day)
            weekday = workday.weekday()

            for idk in num_shift:
                if shift == idk[0]:
                    if weekday == 6 and row[7] == 'F':
                        #escala fixa tem direito a 2x no domingo
                        d = Schedule(valid_on=workday, id_employee=employee, id_workcode=sch_h10 , id_shift=idk[1])
                    else:
                        d = Schedule(valid_on=workday, id_employee=employee, id_workcode=sch_vht , id_shift=idk[1])
                    d.save()

            match shift:
                #Feriados
                case "FE":
                    d = Schedule(valid_on=workday, id_employee=employee, id_workcode=sch_fds)
                    d.save()
                #Folgas
                case "DC" | "DO" | "CH":
                    d = Schedule(valid_on=workday, id_employee=employee, id_workcode=sch_flg)
                    d.save()
                #Férias
                case "FR":
                    d = Schedule(valid_on=workday, id_employee=employee, id_workcode=sch_fer)
                    d.save()

                #Baixas
                case "BM":
                    d = Schedule(valid_on=workday, id_employee=employee, id_workcode='FTB')
                    d.save()
                case 'BS':
                    d = Schedule(valid_on=workday, id_employee=employee, id_workcode='BPS')
                    d.save()
                case 'BP':
                    d = Schedule(valid_on=workday, id_employee=employee, id_workcode='BPT')
                    d.save()

    
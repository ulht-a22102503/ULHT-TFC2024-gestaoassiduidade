import locale
import calendar
import csv
import io
from datetime import datetime
from gestaoassiduidade.models import Schedule

locale.setlocale(locale.LC_ALL, 'pt_PT.utf8')

def memfile_to_list(file):
    new_file = file.read().decode('utf-8')
    reader = csv.reader(io.StringIO(new_file))
    print(next(reader))
    return [line for line in reader]

def import_schedule(file, area):
    #print(file)
    #hmm = memfile_to_list(file)
    #print(hmm)
    num_shift = list
    match area:
        case 'ERPI':
            num_shift = [('M',1),('T',2),('N',3)]
        case 'SAD':
            num_shift = [('1',4), ('2',5), ('3',6), ('4',7), ('5',8), ('7',9)]
        case 'LAV':
            num_shift = [('A',10), ('B',11), ('C',12), ('M',13), ('M0',14), ('M1',15), ('T',16)]
        case 'COZ':
            num_shift = [('1',17), ('2',18), ('A',19), ('B',20)]


    #with open(filename, newline='', encoding='utf-8') as csvfile:
    csvfile = file.read().decode('utf-8')
    reader = csv.reader(io.StringIO(csvfile), delimiter=';', quotechar='|')
    schedule_month = next(reader)[8]
    workday = datetime.strptime(schedule_month,'%B %Y')
    offset = 8 + calendar.monthrange(workday.year, workday.month)[1]
    next(reader)
    for row in reader:
        print("ID trabalhador:", row[0], "| Nome trabalhador:", row[1])
        employee_schedule = row[8:offset]
        print(employee_schedule,'\n')
        for day, shift in enumerate(employee_schedule, start=1):
            workday = workday.replace(day=day)
            weekday = workday.weekday()

            for idk in num_shift:
                if shift == idk[0]:
                    if weekday == 6 and row[7] == 'F':
                        #escala fixa tem direito a 2x no domingo
                        d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='H10' , id_shift=idk[1])
                    else:
                        d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='VHT' , id_shift=idk[1])
                    d.save()

            match shift:
                #Feriados
                case "FE":
                    d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='FDS')
                    d.save()
                #Folgas
                case "DC" | "DO" | "CH":
                    d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='FLG')
                    d.save()
                #Férias
                case "FR":
                    d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='FER')
                    d.save()

                #Baixas
                case "BM":
                    d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='FTB')
                    d.save()
                case 'BS':
                    d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='BPS')
                    d.save()
                case 'BP':
                    d = Schedule(valid_on=workday, id_employee=row[0], id_workcode='BPT')
                    d.save()
    
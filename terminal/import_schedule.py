import locale
import calendar
import csv
import dal_terminal_db as database
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_PT.utf8')

with open('upload.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
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

            match shift:
                #Turno manhã
                case "M":
                    if weekday == 6 and row[7] == 'F':
                        #escala fixa tem direito a 2x no domingo
                        database.insert_schedule(row[0],workday,'H10',1)
                    else:
                        database.insert_schedule(row[0],workday,'VHT',1)

                #Turno tarde
                case "T":
                    if weekday == 6 and row[7] == 'F':
                        #escala fixa tem direito a 2x no domingo
                        database.insert_schedule(row[0],workday,'H10',2)
                    else:
                        database.insert_schedule(row[0],workday,'VHT',2)

                #Turno noite
                case "N":
                    if weekday == 6 and row[7] == 'F':
                        #escala fixa tem direito a 2x no domingo
                        database.insert_schedule(row[0],workday,'H10',3)
                    else:
                        database.insert_schedule(row[0],workday,'VHT',3)
                
                #Feriados
                case "FE":
                    database.insert_schedule(row[0],workday,'FDS')
                #Folgas
                case "DC" | "DO" | "CH":
                    database.insert_schedule(row[0],workday,'FLG')
                #Férias
                case "FR":
                    database.insert_schedule(row[0],workday,'FER')

                #Baixas
                case "BM":
                    database.insert_schedule(row[0],workday,'FTB')
                case 'BS':
                    database.insert_schedule(row[0],workday,'BPS')
                case 'BP':
                    database.insert_schedule(row[0],workday,'BPT')
    
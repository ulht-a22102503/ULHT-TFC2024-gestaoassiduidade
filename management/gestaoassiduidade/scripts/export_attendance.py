import xlsxwriter
from io import BytesIO
#import dal_terminal_db as database
from datetime import datetime, timedelta
from gestaoassiduidade.models import Employee, Schedule, Attendance, Shift

def export_attendance(start_date, end_date):
    start_date = datetime.strptime(start_date,'%d-%m-%Y')
    end_date = datetime.strptime(end_date,'%d-%m-%Y')

    # Create an new Excel file and add a worksheet.
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True,})
    format_time = workbook.add_format({'num_format':'HH:MM:SS'})

    filtered_schedule = Schedule.objects.values('id_employee').filter(
        valid_on__gte=start_date, valid_on__lte=end_date).distinct().order_by('id_employee')
    print("Num funcionarios com escala",len(filtered_schedule))

    # Create a format to use in the merged range.
    merge_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "fg_color": "yellow",
        }
    )

    col_topo = [("A1:A2",'dia'), ("B1:C1",'entrada'), ("D1:E1",'início de pausa'), ("F1:G1",'fim de pausa'), ("H1:I1",'saída'),("J1:J2",'código'),('K1:K2','Tempo trabalhado'),('L1:L2','Tempo descansado')]
    col_topo2 = ['','registado','esperado','registado','esperado','registado','esperado','registado','esperado',]

    for line in filtered_schedule:
        current_employee = line['id_employee']

        worksheet = workbook.add_worksheet(str(current_employee))
        #worksheet.set_column("A:L",13)

        # Criar cabeçalho
        for cols in col_topo:
            worksheet.merge_range(cols[0],cols[1],merge_format)

        for col_num, data in enumerate(col_topo2):
            worksheet.write(1, col_num, data)

        # Obter dados
        filtered_schedule = Schedule.objects.values('valid_on', 'id_workcode', 'id_shift').filter(id_employee=current_employee,valid_on__gte=start_date, valid_on__lte=end_date)
        filtered_attendance = Attendance.objects.values('timestamp').filter(id_employee=current_employee,timestamp__range=(start_date, end_date))
        yummy_data = dict()

        # Juntar dados no mesmo dict para ser mais fácil de trabalhar
        for line in filtered_schedule:
            picagens = [picagem['timestamp'] for picagem in filtered_attendance if picagem['timestamp'].date() == line['valid_on']]
            picagens.sort()
            yummy_data[line['valid_on']] = (line['id_workcode'],line['id_shift'], picagens)

        # Preencher com dados
        for day in range(0, (end_date - start_date).days+1):
            current_day = (start_date + timedelta(days=day))
            worksheet.write(day+2,0,str(current_day.date()))

            if current_day.date() in yummy_data.keys():
                # Código de trabalho
                worksheet.write(day+2,9,yummy_data[current_day.date()][0])
                # Escala
                if yummy_data[current_day.date()][1] is None:
                    for fill in range(2,9,2):
                        worksheet.write(day+2,fill,'N/A')
                else:
                    shift = Shift.objects.get(id_shift=yummy_data[current_day.date()][1])
                    worksheet.write(day+2,2,getattr(shift,'time_begin').strftime('%HH:%MM:%SS'),format_time)
                    worksheet.write(day+2,4,getattr(shift,'break_begin').strftime('%HH:%MM:%SS'),format_time)
                    worksheet.write(day+2,6,getattr(shift,'break_end').strftime('%HH:%MM:%SS'),format_time)
                    worksheet.write(day+2,8,getattr(shift,'time_end').strftime('%HH:%MM:%SS'),format_time)

                # Picagens
                idx = 1
                for fill in yummy_data[current_day.date()][2]:
                        worksheet.write(day+2,idx,fill.strftime('%HH:%MM:%SS'),format_time)
                        idx +=2
                if len(yummy_data[current_day.date()][2]) == 4:
                    worksheet.write(day+2,11,str(yummy_data[current_day.date()][2][2]-yummy_data[current_day.date()][2][1]))
                    worksheet.write(day+2,10,str(yummy_data[current_day.date()][2][3]-yummy_data[current_day.date()][2][0]))
                    #worksheet.write_formula(f'L{day+3}',f'=F{day+3} - D{day+3}',format_time) #Tempo de descanso
                    #worksheet.write_formula(f'K{day+3}',f'=(H{day+3} - B{day+3}) - L{day+3}',format_time) #Tempo de trabalho
            worksheet.autofit()

    workbook.close()
    return output.getvalue()

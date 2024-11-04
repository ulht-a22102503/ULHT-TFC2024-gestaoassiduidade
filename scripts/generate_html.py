import csv

#Auxiliary stuff
def dump_employees():
    employees = {}

    with open('./data/employees.csv', newline='') as employees_csv:
        employee_fields = ['IDfunc', 'IDfinger', 'Name']
        
        reader = csv.DictReader(employees_csv, fieldnames = employee_fields)
        for row in reader:
            employees[row['IDfunc']] = row['Name']

    return employees


def generate_from_csv():
    html = '<h1>Picagens de funcionários</h1>\n'
    employees = dump_employees()

    html+='<table>\n<tr><td>Funcionário</td><td>Hora de picagem</td></tr>\n'
    with open('./data/fingerprint_log.csv',newline='') as fingerprints_csv:
        fingerprint_fields = ['IDfunc','timestamp']
        reader = csv.DictReader(fingerprints_csv, fieldnames = fingerprint_fields)

        for row in reader:
            html+=f"<tr><td>{employees.get(row['IDfunc'])}</td><td>{row['timestamp']}</td></tr>\n"
    
    html+='</table>'
    return html


f = open("./web/index.html", "w", encoding="utf-8")
f.write(generate_from_csv())
f.close()
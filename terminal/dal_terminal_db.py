import mariadb

def connect_to_db():
    conn = mariadb.connect(
    user="assiduidade",
    password="password",
    host="localhost",
    database="terminal")
    return conn

#retrieving information 
def get_employee_from_fingerprint(conn, ID_finger):
    cur = conn.cursor()
    cur.execute("SELECT credentials.ID_employee, `name` FROM credentials INNER JOIN employee ON credentials.ID_employee = employee.ID_employee WHERE ID_sensor_index_main=? OR ID_sensor_index_sec=?", (ID_finger,ID_finger,))
    employee_data = set()
    if cur.rowcount != 0:
        employee_data = cur.fetchone()
    conn.close()
    return employee_data

def get_login_match(conn, ID_func, secret_code):
    cur = conn.cursor()
    cur.execute("SELECT credentials.ID_employee, `name` FROM credentials INNER JOIN employee ON credentials.ID_employee = employee.ID_employee WHERE credentials.ID_employee=? AND pincode=SHA2(?,256)", (ID_func, secret_code,))
    employee_data = set()
    if cur.rowcount != 0:
        employee_data = cur.fetchone()
    conn.close()
    return employee_data

def does_func_exist(conn, ID_func):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(ID_employee) FROM employee WHERE ID_employee=?", (ID_func,))
    ID_func = cur.fetchone()
    conn.close()

    if ID_func == None:
        return False
    return True

def get_func_fingers(conn, ID_func):
    cur = conn.cursor()
    cur.execute("SELECT ID_sensor_index_main, ID_sensor_index_sec FROM credentials WHERE ID_employee=?", (ID_func,))
    fingers = (cur.ID_sensor_index_main, cur.ID_sensor_index_sec)
    conn.close()
    return fingers

def get_today_schedule(conn, ID_func):
    cur = conn.cursor()
    cur.execute("SELECT time_begin, break_begin, break_end, time_end FROM schedule INNER JOIN shift ON schedule.ID_shift = shift.ID_shift WHERE ID_employee = ? AND valid_on = CURDATE()", (ID_func,))
    times = set()
    if cur.rowcount != 0:
        times = (cur.time_begin, cur.break_begin, cur.break_end, cur.time_end)
    conn.close()
    return times

def get_today_attendance(conn, ID_func):
    cur = conn.cursor()
    cur.execute("SELECT `timestamp` FROM attendance WHERE ID_employee=? AND `timestamp` >= CURDATE()", (ID_func,)) #Apenas precisa de acontecer depois da meia noite
    att_recs = [record for record in cur]
    conn.close()
    return att_recs

#insert information
def insert_attendence(conn, ID_func):
    try: 
        conn.cursor().execute("INSERT INTO attendance (ID_employee,`timestamp`) VALUES (?, NOW())", (ID_func,))
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()

def insert_schedule(conn, ID_func, day, workcode, shift=None):
    try:
        if shift is None:
            conn.cursor().execute("INSERT INTO schedule (ID_employee,valid_on,ID_workcode) VALUES (?, ?, ?)", (ID_func, day, workcode))
            conn.commit()
        else:
            conn.cursor().execute("INSERT INTO schedule (ID_employee,valid_on,ID_workcode,ID_shift) VALUES (?, ?, ?, ?)", (ID_func, day, workcode, shift))
            conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()

def insert_finger(conn, ID_employee, ID_index):
    try: 
        conn.cursor().execute("INSERT INTO credentials (ID_employee,ID_index_main) VALUES (?, ?)", (ID_employee, ID_index))
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()

def insert_alt_finger(conn, ID_employee, ID_index):
    try: 
        conn.cursor().execute("UPDATE credentials SET ID_sensor_index_sec=? WHERE ID_employee=?", (ID_employee, ID_index))
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()

def insert_pincode(conn, ID_employee, secret_code):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM credentials WHERE ID_employee=?", (ID_employee,))
    func_auth_exists = cur.fetchone()[0]
    conn.close()

    try: 
        if func_auth_exists == True:
            conn.cursor().execute("UPDATE credentials SET pincode=? WHERE ID_employee=?", (secret_code, ID_employee,))
        else:
            conn.cursor().execute("INSERT INTO credentials (ID_employee,pincode) VALUES (?, ?)", (ID_employee, secret_code))
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()
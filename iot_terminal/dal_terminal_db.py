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
    cur.execute("SELECT ID_employee FROM credentials WHERE ID_sensor_index_main=? OR ID_sensor_index_sec=?", (ID_finger,ID_finger,))
    ID_func = cur.fetchone()[0]
    conn.close()
    return ID_func

def get_login_match(conn, ID_func, secret_code):
    cur = conn.cursor()
    cur.execute("SELECT ID_employee FROM credentials WHERE ID_employee=? AND pincode=SHA2(?,256)", (ID_func, secret_code,))
    result = cur.fetchone()
    conn.close()

    if result == None:
        return -1
    return result[0]

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
    fingers = (cursor.ID_sensor_index_main, cursor.ID_sensor_index_sec)
    conn.close()
    return fingers

#insert information
def insert_attendence(conn, ID_func):
    try: 
        conn.cursor().execute("INSERT INTO attendance (ID_employee,timestamp) VALUES (?, NOW())", (ID_func,))
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
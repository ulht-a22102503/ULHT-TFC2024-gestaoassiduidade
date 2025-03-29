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

def get_login_match(conn, secret_code):
    cur = conn.cursor()
    cur.execute("SELECT ID_employee FROM credentials WHERE pincode=SHA2(?,256)", (secret_code,))
    result = cur.fetchone()[0]
    conn.close()

    if result is null or result == '':
        return -1
    return result

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
    

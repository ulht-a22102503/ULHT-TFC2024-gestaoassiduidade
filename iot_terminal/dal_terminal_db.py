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
    cur.execute("SELECT ID_employee FROM fingerprints WHERE ID_fingerprint=?", (ID_finger,))
    ID_func = cur.fetchone()[0]
    conn.close()
    return ID_func

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
        conn.cursor().execute("INSERT INTO fingerprints (ID_employee,ID_index) VALUES (?, ?)", (ID_employee, ID_index))
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()

#print(f"Last Inserted ID: {cur.lastrowid}")
    

import mariadb

def connect_to_db():
    conn = mariadb.connect(
    user="assiduidade",
    password="password",
    host="localhost",
    database="terminal")
    return conn

#retrieving information 
def get_employee_from_fingerprint(conn, ID_fingerprint):
    cursor().execute("SELECT ID_employee FROM fingerprints WHERE ID_fingerprint=?", (ID_fingerprint,))
    row= cursor.fetchone()
    print(*row)
    conn.close()

#insert information
def insert_attendence(conn, ID_employee):
    try: 
        cursor().execute("INSERT INTO attendance (ID_employee,timestamp) VALUES (?, NOW())", (ID_employee))
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()

def insert_finger(conn, ID_employee, ID_index):
    try: 
        cursor().execute("INSERT INTO fingerprints (ID_employee,ID_index) VALUES (?, ?)", (ID_employee, ID_index))
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.close()

#print(f"Last Inserted ID: {cur.lastrowid}")
    

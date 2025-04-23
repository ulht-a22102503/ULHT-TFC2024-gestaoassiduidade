import eel
import json
from playaudio import playaudio
import fingerprint_functionality as fpSensor
import dal_terminal_db as database

def auth_finger(finger_reader, db_conn):
    fp_idx = fpSensor.read(finger_reader)
    db_conn = database.connect_to_db()
    func = database.get_employee_from_fingerprint(conn,fp_idx)
    print("ID do funcionario",func)
    db_conn = database.connect_to_db()
    database.insert_attendence(db_conn,func)
    payload = {
        "auth": "success",
        "type": "fingerprint",
        "id": func,
        "name": "Funcionário",
        "issues": 0,
    }
    playaudio('start-sound-beep-102201.mp3') #Passar isto para uma função diferente
    return json.dumps(payload)


def auth_pin(payload):
    db_conn = database.connect_to_db()
    result = database.get_login_match(db_conn, payload['secret_code'])
    if result == -1:
        auth_res = "failure"
    else:
        auth_res = "success"
        db_conn = database.connect_to_db()
        database.insert_attendence(db_conn,result)
    payload_produce = {
        "auth": auth_res,
        "type":"PIN",
        "id": result,
        "name": "Funcionário",
        "issues": 0,
    }
    playaudio('start-sound-beep-102201.mp3') #Passar isto para uma função diferente
    return payload_produce


def enroll(finger_reader, db_conn, func_id):
    db_conn = database.connect_to_db()
    result = database.does_func_exist(db_conn, func_id)
    if result == False:
        print('Esse trabalhador não existe')
    fp_idx = fpSensor.enroll(finger_reader)
    database.insert_finger(db_conn,func_id,fp_idx)
    playaudio('start-sound-beep-102201.mp3') #Passar isto para uma função diferente


def main():
    #finger_reader = fpSensor.init_reader()
    eel.init('web') #define a pasta com  o UI html
    eel.expose(auth_pin)
    eel.start('menu.html') #começa o webserver


if __name__ == '__main__':
    main()
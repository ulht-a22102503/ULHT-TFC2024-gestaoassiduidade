import eel
import json
from playsound3 import playsound
import datetime
import fingerprint_functionality as fpSensor
import dal_terminal_db as database

def auth_finger():
    try:
        finger_reader = fpSensor.init_reader()
        fp_idx = fpSensor.read(finger_reader)
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        playsound("audio/3-beeps.mp3", block=False)
        return json.dumps({"auth": "failure"})
    
    if fp_idx is None or fp_idx < 0:
        playsound("audio/3-beeps.mp3", block=False)
        return json.dumps({"auth": "failure"})

    db_conn = database.connect_to_db()
    func = database.get_employee_from_fingerprint(db_conn,fp_idx)
    print("ID do funcionario",func)
    db_conn = database.connect_to_db()
    database.insert_attendence(db_conn,func)
    #obter picagens das últimas 26 horas
    db_conn = database.connect_to_db()
    database.get_today_attendance(db_conn, func)
    #obter horário
    db_conn = database.connect_to_db()
    database.get_today_schedule(db_conn, func)
    #lógica para verificar anomalias
    issue_cnt = check_anomalies(None, None)
    payload = {
        "auth": "success",
        "type": "fingerprint",
        "id": func,
        "name": "Funcionári@",
        "issues": issue_cnt,
    }
    if issue_cnt == 0:
        playsound("audio/1-beep.mp3", block=False)
    else:
        playsound("audio/2-beeps.mp3", block=False)
    return json.dumps(payload)


def auth_pin(payload):
    db_conn = database.connect_to_db()
    result = database.get_login_match(db_conn, payload['id'], payload['secret_code'])
    issue_cnt = 0
    if result == -1:
        auth_res = "failure"
        playsound("audio/3-beeps.mp3", block=False)
    else:
        auth_res = "success"
        db_conn = database.connect_to_db()
        database.insert_attendence(db_conn,result)
        #obter picagens das últimas 26 horas
        db_conn = database.connect_to_db()
        database.get_today_attendance(db_conn, payload['id'])
        #obter horário
        db_conn = database.connect_to_db()
        database.get_today_schedule(db_conn, payload['id'])
        #lógica para verificar anomalias
        issue_cnt = check_anomalies(None, None)
    payload_produce = {
        "auth": auth_res,
        "type":"PIN",
        "id": payload['id'],
        "name": "Funcionári@",
        "issues": issue_cnt,
    }
    if issue_cnt == 0:
        playsound("audio/1-beep.mp3", block=False)
    else:
        playsound("audio/2-beeps.mp3", block=False)
    return payload_produce


def enroll(func_id):
    finger_reader = fpSensor.init_reader()
    db_conn = database.connect_to_db()
    result = database.does_func_exist(db_conn, func_id)
    if result == False:
        #indicar que o trabalhador não existe
        print('O trabalhador não existe')
    
    #verificar se o funcionário existe na tabela credentials ou se a impressão digital secundária é -1
    fingers = database.get_func_fingers(db_conn, result)
    fp_type = str
    if fingers == None:
        fp_type = 'primary'
    elif fingers[0] > 0 and fingers[0] == -1:
        fp_type = 'alternative'
    
    #mostrar no ecrã para colocar dedo

    #construir o modelo para a impressão digital
    # 1) enroll parte 1 para a 1ª leitura
    fp_cnt = fpSensor.enroll_part1(finger_reader)
    # 2) mostrar no ecrã para tirar dedo
    eel.updateText("Retire o dedo do sensor")
    # 3) esperar 3 segundos e mostrar no ecrã para colocar dedo novamente
    eel.sleep(3.0)
    eel.updateText("Coloque o dedo novamente no sensor")
    # 4) enroll parte 2 para 2ª leitura
    fp_idx = fpSensor.enroll_part2(finger_reader,fp_cnt)
    # 5) em caso de sucesso, guardar o índice para o dedo na BD
    enroll = str
    if fp_idx != -1:
        enroll = "success"
        if fp_type == "primary":
            database.insert_finger(db_conn,func_id,fp_idx)
        else:
            database.insert_alt_finger(db_conn,func_id,fp_idx)
        playsound("audio/1-beep.mp3", block=False)
    else:
        enroll = "failure"
        playsound("audio/3-beeps.mp3", block=False)
    # 6) mostrar informação de erro/sucesso e voltar ao menu
    payload = {
        "enroll": status,
    }
    return payload

def check_anomalies(schedule, att_records):
    anomaly_cnt = 0
    if schedule is None and att_records != 0:
        #não era esperado o trabalhador estar ao serviço
        return 4

    currently = datetime.datetime.now()
    #ver quantas picagens eram esperadas até ao momento
    att_expected = len([expected for shift_time in schedule if shift_time <= currently.time])
    if att_expected != att_records:
        #existem x picagens em falta
        anomaly_cnt+=abs(att_expected-att_records)

    #existem registos, mas estão fora da tolerância
    tolerance = datetime.timedelta(minutes=15)
    for shift_time in att_expected:
        if (attendance in att_records) < (shift_time - tolerance) or (shift_time + tolerance) > (attendance in att_records):
            anomaly_cnt+=1

    return anomaly_cnt

def keep_running():
    pass

def main():
    #finger_reader = fpSensor.init_reader()
    eel.init('web') #define a pasta com  o UI html
    eel.expose(auth_pin)
    eel.expose(auth_finger)
    eel.start('menu.html', close_callback= keep_running) #começa o webserver


if __name__ == '__main__':
    main()
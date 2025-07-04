import eel
import json
from playsound3 import playsound
import datetime
import logging
import sys

import fingerprint_functionality as fpSensor
import dal_terminal_db as database

logger = logging.getLogger(__name__)

def auth_finger():
    logger.info("Got a request to mark attendance with fingerprint")
    try:
        finger_reader = fpSensor.init_reader()
        fp_idx = fpSensor.read(finger_reader)
    except Exception as e:
        logger.error("Operation failed! " + str(e))
        playsound("audio/3-beeps.mp3", block=False)
        return json.dumps({"auth": "failure", "type": "fingerprint"})
    
    if fp_idx is None or fp_idx < 0:
        playsound("audio/3-beeps.mp3", block=False)
        return json.dumps({"auth": "failure"})

    db_conn = database.connect_to_db()
    func = database.get_employee_from_fingerprint(db_conn,fp_idx)
    logger.debug(f"Sucessfully authenticated employee nr. {func[0]}")
    db_conn = database.connect_to_db()
    database.insert_attendence(db_conn,func)
    logger.debug("Attendance sucessfully registered")
    #obter picagens das últimas 26 horas
    db_conn = database.connect_to_db()
    attendance = database.get_today_attendance(db_conn, func)
    #obter horário
    db_conn = database.connect_to_db()
    schedule = database.get_today_schedule(db_conn, func)
    logger.debug(f"Today's schedule for employee {func[0]}")
    logger.debug(f"Today's attendence records for employee {func[0]}")
    #lógica para verificar anomalias
    issue_cnt = check_anomalies(schedule, attendance)
    logger.debug(f"Found {issue_cnt} anomalies for employee {func[0]}")
    payload = {
        "auth": "success",
        "type": "fingerprint",
        "id": func[0],
        "name": func[1],
        "issues": issue_cnt,
    }
    if issue_cnt == 0:
        playsound("audio/1-beep.mp3", block=False)
    else:
        playsound("audio/2-beeps.mp3", block=False)
    return json.dumps(payload)


def auth_pin(payload):
    logger.info("Got a request to mark attendance with PIN code")
    db_conn = database.connect_to_db()
    result = database.get_login_match(db_conn, payload['id'], payload['secret_code'])
    issue_cnt = 0
    if len(result) == 0:
        result = (payload['id'], "Funcionári@ desconhecid@")
        logger.debug(f"Credentials provided for employee nr. {payload['id']} are incorrect")
        auth_res = "failure"
        playsound("audio/3-beeps.mp3", block=False)
    else:
        logger.debug(f"Credentials provided for employee nr. {payload['id']} are correct")
        auth_res = "success"
        db_conn = database.connect_to_db()
        database.insert_attendence(db_conn,result[0])
        logger.debug("Attendance sucessfully registered")
        #obter picagens das últimas 26 horas
        db_conn = database.connect_to_db()
        attendance = database.get_today_attendance(db_conn, payload['id'])
        #obter horário
        db_conn = database.connect_to_db()
        schedule = database.get_today_schedule(db_conn, payload['id'])
        logger.debug(f"Today's schedule for employee {result[0]}")
        logger.debug(f"Today's attendence records for employee {result[0]}")
        #lógica para verificar anomalias
        issue_cnt = check_anomalies(schedule, attendance)
        logger.debug(f"Found {issue_cnt} anomalies for employee {result[0]}")
    payload_produce = {
        "auth": auth_res,
        "type":"PIN",
        "id": result[0],
        "name": result[1],
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
    print("Schedule:",schedule, type(schedule))
    print("Attendance:",att_records, type(att_records))

    anomaly_cnt = 0
    currently = datetime.datetime.now()

    #ver quantas picagens eram esperadas até ao momento
    att_expected = [expected for shift_time in schedule if shift_time <= currently.time]
    if len(att_expected) != len(att_records):
        #existem x picagens em falta
        anomaly_cnt+=abs(len(att_expected)-len(att_records))

    #existem registos, mas estão fora da tolerância
    tolerance = datetime.timedelta(minutes=15)
    for shift_time in att_expected:
        if (attendance in att_records) < (shift_time - tolerance) or (shift_time + tolerance) > (attendance in att_records):
            anomaly_cnt+=1

    return anomaly_cnt

def keep_running():
    logger.debug("Close callback executed. Keeping the application alive.")
    pass

def main():    
    log_filename = f'log/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}-terminal.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format="[{asctime}] [{levelname}] {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S",filemode='w')

    logger.info("Initializing...")
    finger_reader = fpSensor.init_reader()
    eel.init('web') #define a pasta com o UI HTML
    eel.expose(auth_pin)
    eel.expose(auth_finger)
    logger.info("Ready!")
    eel.start('menu.html', close_callback= keep_running, cmdline_args=['--start-fullscreen']) #começa o webserver


if __name__ == '__main__':
    main()
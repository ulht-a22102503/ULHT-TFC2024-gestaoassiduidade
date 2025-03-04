#!/usr/bin/env python

from websockets.sync.server import serve

import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
import json

import dal_terminal_db as database

#Funções para fazer algo com o sensor de impressão digital
def fingerprint_read(websocket):
    #Inicialização do sensor
    try:
        fp = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( fp.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)
    
    try:
        print('Waiting for finger...')

    ## Wait that finger is read
        while ( fp.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        fp.convertImage(FINGERPRINT_CHARBUFFER1)

        ## Searchs template
        result = fp.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            return
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return

    conn = database.connect_to_db()
    func = database.get_employee_from_fingerprint(conn,int(positionNumber))
    print("ID do funcionario",func)
    conn = database.connect_to_db()
    database.insert_attendence(conn,func)
    payload = {
        "auth": "success",
        "id": func,
        "name": "Funcionário",
        "issues": 0,
    }
    websocket.send(json.dumps(payload))
    return


def echo(websocket):
    for message in websocket:
        websocket.send(message)


def main():
    with serve(fingerprint_read, "localhost", 8765) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()

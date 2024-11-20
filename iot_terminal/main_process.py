from gpiozero import Button
from signal import pause

import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

import dal_terminal_db as database

#Funções para fazer algo com o sensor de impressão digital
def fingerprint_enroll():
    func = int(input("Qual o ID do funcionario? "))
    
    try:
        print('Waiting for finger...')

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(FINGERPRINT_CHARBUFFER2)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return

    conn = database.connect_to_db()
    database.insert_finger(conn,func,int(positionNumber))

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

def fingerprint_read(fp):
    try:
        #print('Waiting for finger...')

    ## Wait that finger is read
        #while ( f.readImage() == False ):
        #    pass

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
    return

#Inicialização GPIO
fingerprint_touch = Button(23)
button = Button(24)

#Inicialização do sensor
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

#Execução permanente do script
while True:
    if f.readImage() == True:
        fingerprint_read(f)
        time.sleep(1)
    elif button.is_pressed:
        fingerprint_enroll()

pause()

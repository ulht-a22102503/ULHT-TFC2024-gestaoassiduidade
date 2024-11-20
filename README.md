# ULHT-TFC2024-gestaoassiduidade
Trabalho final de curso - Aplicação de gestão de assiduidade

# Install
## Requirements
- Raspberry Pi
- Fingerprint sensor
- MariaDB
- Python 3
- Django

This guide was tested on a Raspberry Pi 4 running RaspberryOS 64-bit

Begin by cloning this repository to the RPi.
```bash
git clone https://github.com/ulht-a22102503/ULHT-TFC2024-gestaoassiduidade.git
```

### Fingerprint sensor
To be able to use the fingerprint sensor, the **Serial interface** has to be enabled. This can be done through `raspi-config` -> Interface Options -> Serial Port. Make sure the Serial Monitor is disabled!

### MariaDB
Start by installing the MariaDB engine

```bash
sudo apt-get update
sudo apt install mariadb-server
```

Go through the setup with `sudo mysql_secure_installation`. Then connect to MariaDB and run the database script. Also, create the user with permission to access it

```bash
pi@raspberrypi: sudo mysql
MariaDB [(none)]> source <path to terminal_db.sql script>;
MariaDB [(none)]> GRANT INSERT, SELECT, UPDATE, DELETE ON terminal.* TO 'assiduidade'@'localhost' IDENTIFIED BY 'password';
MariaDB [(none)]> exit
```

### Python
Next, we'll cover the python environment to run the code to access the fingerprint sensor.
Start by ensuring Python and pip are installed

```bash
sudo apt-get update
sudo apt install python3 python3-pip python3-venv
```

Then create a folder where the virtual environments will be created. At the end of each block you'll have a running process, so it's recommended to run them in seperate terminal tabs/windows

Before starting, install the MariaDB connector dependencies

```bash
sudo apt-get update
sudo apt install gcc python3-dev openssl curl
curl -LsSO https://r.mariadb.com/downloads/mariadb_repo_setup
echo "6083ef1974d11f49d42ae668fb9d513f7dc2c6276ffa47caed488c4b47268593  mariadb_repo_setup" \
    | sha256sum -c -
chmod +x mariadb_repo_setup
```

With the pre-requisites met, setup the virtual environment

```bash
python3 -m venv .venv_fingerprint
source .venv_fingerprint/bin/activate
pip install -r <path to terminal_requirements.txt>
```

Now run the script that will be responsible for the fingerprint sensor functionality

```bash
cd <path to iot_terminal folder from this repo>
python3 main_process.py
```

### Django
The process for django is similar

```bash
python3 -m venv .venv_fingerprint
source .venv_fingerprint/bin/activate
pip install -r <path to terminal_requirements.txt>
cd <path to web folder from this repo>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
# ULHT-TFC2024-gestaoassiduidade

Trabalho final de curso - Aplicação de gestão de assiduidade

# Install

## Requirements

- Raspberry Pi
- Fingerprint sensor
- MariaDB
- Python 3
- Django

This guide was tested on a Raspberry Pi 4 and Raspberry Pi 5 running RaspberryOS 64-bit

Begin by cloning this repository to the RPi.

```bash
git clone https://github.com/ulht-a22102503/ULHT-TFC2024-gestaoassiduidade.git
```

### Fingerprint sensor

To be able to use the fingerprint sensor, the **Serial interface** has to be enabled. This can be done through `raspi-config` -> Interface Options -> Serial Port. Make sure the Serial Monitor is disabled!

### Install script

Run the script in the root of the repository you've just cloned. It will take care of most configurations

```bash
chmod +x first_setup.sh
./first_setup.sh
```

### Starting the local server

To run, you must go to `$HOME/Documents/` and activate the venv. Then navigate to the repository folder and run the script responsible for most of the functionality.

```bash
.iot_terminal-venv/bin/activate
cd <repository_folder>/iot_terminal
python3 eel-server.py`
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

# Docs

## Terminal backend

The backend mainly works with JSON payloads, check the [.md file](/iot_terminal/payload_format.md) with the format for each function.

#!/bin/bash
#update packages
echo "1/5 Updating packages"
sudo apt-get update
sudo apt-get upgrade

#install dependencies
echo "2/5 Installing dependencies"
sudo apt install python3 python3-pip python3-venv mariadb-server libmariadb-dev

#setup database
echo "3/5 Setting up database"
sudo mysql -e "source terminal/terminal_db.sql;"
sudo mysql -e "GRANT INSERT, SELECT, UPDATE, DELETE ON terminal.* TO 'assiduidade'@'localhost' IDENTIFIED BY 'password';"
exit

#create venv
echo "4/5 Creating python venvs"
python3 -m venv $HOME/Documents/.terminal-venv
python3 -m venv $HOME/Documents/.web-venv

#install venv dependencies
echo "5/5 Installing python dependencies"
source "$HOME/Documents/.terminal-venv/bin/activate"
pip install -r terminal_requirements.txt
deactivate

source "$HOME/Documents/.web-venv/bin/activate"
pip install -r web_requirements.txt
deactivate

echo "Done! You can now enable the venv and run the websocket-server.py file"
@echo off
pip install -r requirement.txt
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
python migrate.py init_user
pause
python app.py
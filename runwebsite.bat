REM Create a virtual environment
echo Creating Python virtual environment...
python -m venv sslp_env

REM Activate the virtual environment
echo Activating Python virtual environment...
call sslp_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install packages from requirements.txt
echo Installing required Python packages...
pip install -r requirements.txt

REM Creating .env file
echo Creating .env file
python create_dot_env.py

REM Change directory to Django project
echo Changing directory to Django project...
cd SSLP_analyzer


REM Run Django server
echo Starting Django server...
start /min python manage.py runserver

REM Open Chrome to Django URL
echo Opening Django URL in Chrome...
start chrome http://127.0.0.1:8000/


REM Deactivate the virtual environment
echo Deactivating Python virtual environment...
call sslp_env\Scripts\deactivate.bat

echo Done.

pause

exit

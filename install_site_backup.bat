REM Create a virtual environment
echo Creating Python virtual environment...
py -m venv sslp_env

REM Activate the virtual environment
echo Activating Python virtual environment...
call sslp_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
py -m pip install --upgrade pip

REM Install packages from requirements.txt
echo Installing required Python packages...
pip install -r requirements.txt

REM Creating .env file
echo Creating .env file
py create_dot_env.py

REM Change directory to Django project
echo Changing directory to Django project...
cd SSLP_analyzer

REM Creating migrations
echo Creating migrations
py manage.py makemigrations

REM Applying migrations
echo Applying migrations
py manage.py migrate

REM Creating User
echo Creating User please create an account (Email is optional)
py manage.py createsuperuser

REM Run Django server
echo Starting Django server...
start /min py manage.py runserver

REM Open Chrome to Django URL
echo Opening Django URL in Chrome...
start chrome http://127.0.0.1:8000/

echo Done.

pause

exit

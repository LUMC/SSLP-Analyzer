REM Activate the virtual environment
echo Activating Python virtual environment...
call sslp_env\Scripts\activate.bat

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
call path\to\your\env\Scripts\deactivate.bat
cd ..

REM Wait for user input
echo Done.


REM End of script
exit

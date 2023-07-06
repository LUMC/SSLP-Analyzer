REM Activate the virtual environment
echo Activating Python virtual environment...
call sslp_env\Scripts\activate.bat

REM Change directory to Django project
echo Changing directory to Django project...
cd SSLP_analyzer

REM Run Django server
echo Starting Django server...
start /min py manage.py runserver


REM Open Chrome to Django URL
echo Opening Django URL in Chrome...
start chrome http://127.0.0.1:8000/

cd ..

REM Wait for user input
echo Done. Server started and website opened!
pause

REM End of script
exit

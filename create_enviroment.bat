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

REM Creating migrations
echo Creating migrations
python manage.py makemigrations

REM Applying migrations
echo Applying migrations
python manage.py migrate

REM Deactivate the virtual environment
echo Deactivating Python virtual environment...
call sslp_env\Scripts\deactivate.bat

echo Done.

pause
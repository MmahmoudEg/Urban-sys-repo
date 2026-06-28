@echo on
F:
cd "F:\mohamed\Law_Firm_Management_system_Django-main\Law_Firm_Management_system_Django-main\"

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Virtual environment activation failed.
    pause
    exit /b
)

python manage.py makemigrations
if errorlevel 1 (
    echo Failed to run makemigrations.
    pause
    exit /b
)

python manage.py migrate
if errorlevel 1 (
    echo Failed to run migrate.
    pause
    exit /b
)

python manage.py runserver
if errorlevel 1 (
    echo Failed to start Django development server.
    pause
    exit /b
)

pause

@echo off

echo ============================
echo FCBQ CALENDAR UPDATE
echo ============================
echo.

cd /d C:\Users\DAVIDGEA\PycharmProjects\fcbq-calendar

call .venv\Scripts\activate.bat

python main.py

git add .

git diff --cached --quiet

if errorlevel 1 (
    git commit -m "Actualitzacio calendaris"
    git push origin main --force
) else (
    echo No hi ha canvis per publicar
)

echo.
echo Proces finalitzat
echo.

pause
@echo off

cd /d C:\Users\DAVIDGEA\PycharmProjects\fcbq-calendar

call .venv\Scripts\activate.bat

python main.py

git add .

git diff --cached --quiet

if errorlevel 1 (
    git commit -m "Actualitzacio %date% %time%"
    git push
) else (
    echo No hi ha canvis per publicar
)

pause
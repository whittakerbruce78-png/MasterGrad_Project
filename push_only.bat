@echo off
echo Отправляем файлы на GitHub...
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/whittakerbruce78-png/MasterGrad_Project.git
"C:\Program Files\Git\cmd\git.exe" push -u origin main
echo Готово! Нажми любую клавишу, чтобы закрыть окно.
pause

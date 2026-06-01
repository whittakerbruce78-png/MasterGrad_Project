@echo off
echo Инициализируем репозиторий...
"C:\Program Files\Git\cmd\git.exe" init

echo Добавляем файлы...
"C:\Program Files\Git\cmd\git.exe" add .

echo Делаем первый коммит...
"C:\Program Files\Git\cmd\git.exe" commit -m "First commit: QA Audit passed"

echo Настраиваем ветку main...
"C:\Program Files\Git\cmd\git.exe" branch -M main

echo Привязываем к твоему репозиторию на GitHub...
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/whittakerbruce78-png/MasterGrad_Project.git

echo Отправляем файлы! Откроется окно авторизации GitHub...
"C:\Program Files\Git\cmd\git.exe" push -u origin main

echo Готово! Нажми любую клавишу, чтобы закрыть окно.
pause

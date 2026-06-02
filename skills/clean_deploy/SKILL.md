---
name: clean-production-deploy-archive
description: >-
  Автоматическая сборка чистого ZIP-архива для публикации сайта на хостинге.
  Скрипт исключает все служебные файлы разработки, логи и скрытые папки репозитория.
---

# Сборка чистого ZIP-архива для публикации (Deploy)

## Обзор
При передаче проекта клиенту или его загрузке по FTP (например, через FileZilla) критически важно отфильтровать файлы, используемые при разработке. Загрузка таких папок как `.git`, временных Python-скриптов локализации, логов тестов или резервных копий снижает безопасность и забивает дисковое пространство хостинга.

Этот скилл содержит стандартизированный Python-скрипт для быстрой и безопасной сборки только рабочего кода.

## Зависимости
- Python 3.x
- Модуль стандартной библиотеки `zipfile`

## Шаблон скрипта сборщика (scripts/build_deploy.py)

Создайте в корне проекта файл скрипта и перечислите только те файлы и директории, которые должны быть отправлены клиенту.

```python
import os
import zipfile

# Директории, которые должны войти в сборку
folders_to_include = [
    'css', 
    'img', 
    'script', 
    'vladivostok-holodilniki', 
    'khabarovsk-holodilniki', 
    'irkutsk-holodilniki'
]

# Отдельные файлы для сборки
files_to_include = [
    'index.html', 
    'index.php', 
    '.htaccess', 
    'robots.txt', 
    'sitemap.xml', 
    'favicon.ico'
]

archive_name = 'Project_Deploy.zip'

def build_zip():
    print(f"Начало сборки архива {archive_name}...")
    
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Добавляем папки и их содержимое
        for folder in folders_to_include:
            if os.path.exists(folder):
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        filepath = os.path.join(root, file)
                        # Сохраняем относительный путь
                        arcname = os.path.relpath(filepath, '.')
                        zip_file.write(filepath, arcname)
                        print(f"[+] Добавлен файл: {arcname}")
                        
        # Добавляем отдельные файлы в корень архива
        for file in files_to_include:
            if os.path.exists(file):
                zip_file.write(file, file)
                print(f"[+] Добавлен файл: {file}")

    print(f"\nСборка успешно завершена! Создан архив: {os.path.abspath(archive_name)}")

if __name__ == "__main__":
    build_zip()
```

## Правила деплоя
1. **Только белый список (Whitelist)**:
   Никогда не используйте архивацию по принципу исключения (blacklist) — например, упаковать всё, кроме `.git`. Вы можете случайно забыть исключить секретные файлы `.env`, приватные ключи или тестовые скрипты. Всегда составляйте список разрешенных папок и файлов (whitelist).
2. **Проверка путей в архиве**:
   Файлы внутри архива должны лежать точно так же, как в корне проекта (без лишних оберточных папок), чтобы при распаковке в `public_html` структура сайта восстановилась верно.
3. **Автоматизация**:
   Запускайте скрипт перед каждой сдачей проекта или обновлением версии.

## Общие ошибки
* **Архивация архива**: Случайное попадание старого файла `.zip` внутрь нового архива из-за упаковки всего корня. Использование whitelisting-подхода полностью решает эту проблему.

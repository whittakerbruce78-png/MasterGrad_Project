import os
import re

html_errors = []
perf_issues = []

# Regex patterns
broken_tag_pattern = re.compile(r'</a>\s*</strong>\s*</a>')
broken_p_pattern = re.compile(r'</p>Мы чиним')
lazy_loading_pattern = re.compile(r'<img(?![^>]*loading=)[^>]*>')

total_images = 0
images_without_lazy = 0

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Syntax checks
            if broken_tag_pattern.search(content):
                html_errors.append(f"{filepath}: Найдена ошибка вложенности тегов (</a></strong></a>)")
            if broken_p_pattern.search(content):
                html_errors.append(f"{filepath}: Найдена ошибка закрытия абзаца (</p>Мы чиним)")
            
            # Performance checks
            imgs = lazy_loading_pattern.findall(content)
            if imgs:
                images_without_lazy += len(imgs)
                total_images += len(re.findall(r'<img[^>]*>', content))

print("=== Ошибки синтаксиса HTML ===")
if html_errors:
    # Print max 10 to not flood
    for err in html_errors[:10]:
        print(err)
    if len(html_errors) > 10:
        print(f"... и еще {len(html_errors) - 10} файлов с такими же ошибками.")
else:
    print("Явных ошибок не найдено.")

print("\n=== Скорость загрузки ===")
print(f"Найдено {images_without_lazy} изображений без атрибута loading='lazy'.")

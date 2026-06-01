import os
import re

pattern = re.compile(r'<h3 (style="[^"]*")>\s*Работаем по всему (Хабаровску|Иркутску), а также по всем районам\s*</h3>', re.DOTALL)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if pattern.search(content):
                    def repl(match):
                        city = match.group(2)
                        new_city = "Хабаровске" if city == "Хабаровску" else "Иркутске"
                        return f'<h3 {match.group(1)}>\n          Работаем в {new_city}, а также по всем районам\n        </h3>'
                        
                    content = pattern.sub(repl, content)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print("Text updated successfully!")

import os
import re

pattern = re.compile(r'(\.district-grid\s*\{[^}]*align-items\s*:\s*)center(\s*;)')
repl = r'\g<1>start\g<2>'

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if pattern.search(content):
                    content = pattern.sub(repl, content)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                pass

print("Alignment fixed!")

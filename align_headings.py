import os
import re

# Match left column heading
left_pattern = re.compile(r'<h3 style="font-size: 24px; color: #222; font-weight: 700; margin-bottom: 10px; text-align: center;">\s*Наш офис г\.Владивосток ул\.Жигура 26а\s*</h3>', re.DOTALL)
left_repl = '<h3 style="font-size: 24px; color: #222; font-weight: 700; margin-top: 0; margin-bottom: 20px; text-align: center;">\n          Наш офис г.Владивосток ул.Жигура 26а\n        </h3>'

# Match right column heading
right_pattern = re.compile(r'<h2 class="district-title">Мы на Картах</h2>')
right_repl = '<h3 class="district-title" style="font-size: 24px; color: #222; font-weight: 700; margin-top: 0; margin-bottom: 20px; text-align: center;">Мы на Картах</h3>'

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changed = False
                if left_pattern.search(content):
                    content = left_pattern.sub(left_repl, content)
                    changed = True
                
                if right_pattern.search(content):
                    content = right_pattern.sub(right_repl, content)
                    changed = True
                    
                if changed:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                pass

print("Headings aligned!")

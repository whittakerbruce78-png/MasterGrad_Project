import os
import re

def fix_dropdown():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                # Fix the issue where the first link (Vladivostok) incorrectly says "г. Иркутск" or "г. Хабаровск"
                # It should look like this:
                # <a href="/" style="...">г. Владивосток</a> or <a href="/">г. Владивосток</a>
                
                # Match lines like: <a href="/" style="font-weight:bold; color:#0066cc;">г. Иркутск</a>
                # Or <a href="/">г. Хабаровск</a>
                
                # Replace inside city-dropdown-content
                def replace_dropdown(match):
                    dropdown = match.group(0)
                    dropdown = re.sub(r'<a href="/"([^>]*)>г\.\s*(Иркутск|Хабаровск)</a>', r'<a href="/"\1>г. Владивосток</a>', dropdown)
                    return dropdown
                
                new_content = re.sub(r'<div class="city-dropdown-content">.*?</div>', replace_dropdown, content, flags=re.DOTALL)
                
                if new_content != content:
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(new_content)

if __name__ == '__main__':
    fix_dropdown()

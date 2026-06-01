import os
import re

def fix_grammar():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                original_content = content
                
                content = re.sub(r'\bво\s+Хабаровске\b', 'в Хабаровске', content)
                content = re.sub(r'\bВо\s+Хабаровске\b', 'В Хабаровске', content)
                
                content = re.sub(r'\bво\s+Иркутске\b', 'в Иркутске', content)
                content = re.sub(r'\bВо\s+Иркутске\b', 'В Иркутске', content)
                
                # Also just in case there's "во Хабаровск", "во Иркутск" (unlikely)
                
                if content != original_content:
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(content)

if __name__ == '__main__':
    fix_grammar()

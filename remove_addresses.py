import os
import re

def remove_addresses():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                original_content = content
                
                # The address line looks like: <p>Наш офис г.Иркутск ул.Жигура 26а</p>
                # Or <p>Наш офис г. Владивосток ул. Жигура 26а</p>
                # Or <strong>Наш офис г.Иркутск ул.Жигура 26а</strong>
                # We can just match: <[^>]+>Наш офис.*?ул\..*?</[^>]+>
                
                content = re.sub(r'<p>\s*Наш офис.*?</p>', '', content, flags=re.IGNORECASE)
                content = re.sub(r'Наш офис.*?ул\.Жигура.*?(?=<)', '', content, flags=re.IGNORECASE)
                
                # Specifically clean up exactly "Наш офис г.Иркутск ул.Жигура 26а" or similar
                content = re.sub(r'Наш офис г\.\s*(Владивосток|Иркутск|Хабаровск)\s*ул\.\s*Жигура\s*26а', '', content, flags=re.IGNORECASE)
                content = re.sub(r'<p>\s*</p>', '', content) # remove empty p tags if any
                
                if content != original_content:
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(content)

if __name__ == '__main__':
    remove_addresses()

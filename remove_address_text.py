import os
import re

pattern = re.compile(r'<p style="text-align: center; color: #666; margin-bottom: 15px; font-size: 16px;">\s*Адрес:.*?</p>', re.DOTALL | re.IGNORECASE)

for root, dirs, files in os.walk('.'):
    city = None
    if 'khabarovsk' in root: city = 'khabarovsk'
    elif 'irkutsk' in root: city = 'irkutsk'
    
    if city:
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if pattern.search(content):
                        content = pattern.sub('', content)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

print("Address text removed successfully!")

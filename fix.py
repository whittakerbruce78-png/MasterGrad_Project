import os
import re

def fix_all():
    base_path = '/MasterGrad_Project'
    
    for root, dirs, files in os.walk('.'):
        for f in files:
            fpath = os.path.join(root, f)
            
            if f.endswith('.html'):
                with open(fpath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 1. Fix absolute links to relative for GitHub Pages
                # Find href="/something" and replace with href="/MasterGrad_Project/something"
                # Careful not to replace href="//" or href="http://"
                content = re.sub(r'href="/([^/][^"]*)"', r'href="' + base_path + r'/\1"', content)
                content = re.sub(r'href="/"', r'href="' + base_path + r'/"', content)
                
                # 2. Add address back to Vladivostok pages map section
                if 'владивосток' in fpath.lower() or 'index.html' in fpath:
                    # Find the empty h3 before the map
                    empty_h3 = r'<h3 style="font-size: 24px; color: #222; font-weight: 700; margin-top: 0; margin-bottom: 0px; text-align: center;">\s*</h3>'
                    filled_h3 = r'<h3 style="font-size: 24px; color: #222; font-weight: 700; margin-top: 0; margin-bottom: 0px; text-align: center;">г. Владивосток, ул. Жигура, 26а</h3>'
                    content = re.sub(empty_h3, filled_h3, content)
                
                with open(fpath, 'w', encoding='utf-8') as file:
                    file.write(content)
            
            elif f == 'reviews.js':
                with open(fpath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Replace absolute image paths in JS
                content = content.replace('"/img/', f'"{base_path}/img/')
                
                with open(fpath, 'w', encoding='utf-8') as file:
                    file.write(content)

if __name__ == '__main__':
    fix_all()
    print("Fixes applied successfully.")

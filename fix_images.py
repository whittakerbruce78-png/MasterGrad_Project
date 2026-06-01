import os
import re

def fix_images():
    base_path = '/MasterGrad_Project'
    
    for root, dirs, files in os.walk('.'):
        for f in files:
            fpath = os.path.join(root, f)
            
            if f.endswith('.html'):
                with open(fpath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Replace src="img/...", src="./img/...", src="../img/...", src="/img/..." 
                # with src="/MasterGrad_Project/img/..."
                content = re.sub(r'src="(?:[\./]*|)img/([^"]+)"', r'src="' + base_path + r'/img/\1"', content)
                
                with open(fpath, 'w', encoding='utf-8') as file:
                    file.write(content)

if __name__ == '__main__':
    fix_images()
    print("Images fixed successfully.")

import os

def fix_scripts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace relative paths for script
    content = content.replace('src="./script/', 'src="../script/')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    # Only target subfolders
    if root != '.' and ('khabarovsk' in root or 'irkutsk' in root):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                fix_scripts(filepath)

print("Script paths fixed!")

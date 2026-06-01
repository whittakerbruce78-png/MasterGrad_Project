import os

def fix_paths(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace relative paths with one level up
    content = content.replace('href="./css/', 'href="../css/')
    content = content.replace('src="./img/', 'src="../img/')
    content = content.replace('src="./js/', 'src="../js/')
    # Also fix links to other pages if they were using ./ 
    # But links are usually /... so we only need to worry about assets

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_paths('khabarovsk-stiralnie-mashini/index.html')
fix_paths('irkutsk-stiralnie-mashini/index.html')
print("Paths fixed!")

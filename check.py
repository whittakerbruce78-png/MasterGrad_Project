import os

for d in ['irkutsk-stiralnie-mashini', 'khabarovsk-stiralnie-mashini', 'irkutsk-holodilniki', 'khabarovsk-holodilniki']:
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as f_in:
                    lines = f_in.readlines()
                    for i, line in enumerate(lines):
                        if '<nav id="sidebar"' in line:
                            print(f"{path}")
                            for j in range(i, i+15):
                                if j < len(lines):
                                    if '<li>' in lines[j]:
                                        print(lines[j].strip())

import re

def check_h1(path):
    try:
        content = open(path, encoding='utf-8').read()
        match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        if match:
            print(f"{path}: {match.group(1).strip()}")
        else:
            print(f"{path}: NO H1")
    except Exception as e:
        print(f"Error reading {path}: {e}")

check_h1('irkutsk-stiralnie-mashini/index.html')
check_h1('irkutsk-holodilniki/index.html')
check_h1('khabarovsk-stiralnie-mashini/index.html')
check_h1('khabarovsk-holodilniki/index.html')
check_h1('стиральные-машины-владивосток/index.html')

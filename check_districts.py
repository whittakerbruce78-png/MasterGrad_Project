import re

content = open('irkutsk-holodilniki/index.html', encoding='utf-8').read()
links = re.findall(r'<a[^>]+href=[\'\"]([^\'\"]+)[\'\"][^>]*>([^<]+)</a>', content)
for h, t in links:
    if 'район' in t.lower() or 'raion' in h.lower() or 'район' in h.lower():
        print(h, t)

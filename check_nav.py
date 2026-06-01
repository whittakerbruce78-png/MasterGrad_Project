import re

content = open('irkutsk-stiralnie-mashini/index.html', encoding='utf-8').read()
nav = re.search(r'<nav id="sidebar".*?</nav>', content, re.DOTALL).group(0)
print('\n'.join(re.findall(r'href=[\'\"]([^\'\"]+)', nav)))

import os
import re

def fix_links(filepath):
    # Determine the city for this file
    city = 'vladivostok'
    if 'khabarovsk' in filepath:
        city = 'khabarovsk'
    elif 'irkutsk' in filepath:
        city = 'irkutsk'

    # Define correct URLs
    if city == 'vladivostok':
        urls = {
            'stir': '/стиральные-машины-владивосток/',
            'holod': '/холодильники-владивосток/',
            'vodonagr': '/водонагреватели-владивосток/',
            'posud': '/посудомоечные-машины-владивосток/'
        }
    elif city == 'khabarovsk':
        urls = {
            'stir': '/khabarovsk-stiralnie-mashini/',
            'holod': '/khabarovsk-holodilniki/',
            'vodonagr': '/khabarovsk-vodonagrevateli/',
            'posud': '/khabarovsk-posudomoechnie-mashini/'
        }
    elif city == 'irkutsk':
        urls = {
            'stir': '/irkutsk-stiralnie-mashini/',
            'holod': '/irkutsk-holodilniki/',
            'vodonagr': '/irkutsk-vodonagrevateli/',
            'posud': '/irkutsk-posudomoechnie-mashini/'
        }

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will use regex to find the list items in the sidebar and replace their hrefs
    # The links look like: <li><a href="...">Стиральные машины</a></li>
    # We can just search and replace the hrefs based on the link text!

    # 1. Стиральные машины
    content = re.sub(r'href="[^"]*"([^>]*>Стиральные машины<)', f'href="{urls["stir"]}"\\1', content)
    
    # 2. Холодильники
    content = re.sub(r'href="[^"]*"([^>]*>Холодильники<)', f'href="{urls["holod"]}"\\1', content)
    
    # 3. Водонагреватели
    content = re.sub(r'href="[^"]*"([^>]*>Водонагреватели<)', f'href="{urls["vodonagr"]}"\\1', content)
    
    # 4. Посудомоечные машины
    content = re.sub(r'href="[^"]*"([^>]*>Посудомоечные машины<)', f'href="{urls["posud"]}"\\1', content)

    # Note: the repair block also has <span>Стиральные машины</span> inside the <a> tag
    # Let's use a more robust replacement for the repair block, or just rely on the fact that 
    # we know all possible corrupted URLs:

    possible_corrupted = [
        "/стиральные-машины-владивосток", "/стиральные-машины-khabarovsk", "/стиральные-машины-irkutsk",
        "/холодильники-владивосток", "/холодильники-khabarovsk", "/холодильники-irkutsk",
        "/водонагреватели-владивосткок", "/водонагреватели-владивосток", "/водонагреватели-khabarovsk", "/водонагреватели-irkutsk",
        "/посудомоечные-машины-владивосток", "/посудомоечные-машины-khabarovsk", "/посудомоечные-машины-irkutsk"
    ]
    
    # Actually, the regex above will catch the sidebar (it has ">Стиральные машины</a>")
    # For the repair block, it looks like:
    # <a href="..." class="..." aria-label="...">\n            <span>Стиральные машины</span>
    content = re.sub(r'href="[^"]*"(\s*class="repair-item[^>]*>\s*<span>Стиральные машины</span>)', f'href="{urls["stir"]}"\\1', content)
    content = re.sub(r'href="[^"]*"(\s*class="repair-item[^>]*>\s*<span>Холодильники</span>)', f'href="{urls["holod"]}"\\1', content)
    content = re.sub(r'href="[^"]*"(\s*class="repair-item[^>]*>\s*<span>Водонагреватели</span>)', f'href="{urls["vodonagr"]}"\\1', content)
    content = re.sub(r'href="[^"]*"(\s*class="repair-item[^>]*>\s*<span>Посудомоечные машины</span>)', f'href="{urls["posud"]}"\\1', content)

    # And for the light-theme-block (the text paragraph with links):
    # <a href="..." title="Ремонт стиральных машин на дому во Владивостоке">стиральная машина</a>
    content = re.sub(r'href="[^"]*"([^>]*>стиральная машина<)', f'href="{urls["stir"]}"\\1', content)
    content = re.sub(r'href="[^"]*"([^>]*>холодильник<)', f'href="{urls["holod"]}"\\1', content)
    content = re.sub(r'href="[^"]*"([^>]*>посудомойка<)', f'href="{urls["posud"]}"\\1', content)
    content = re.sub(r'href="[^"]*"([^>]*>водонагреватель<)', f'href="{urls["vodonagr"]}"\\1', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            fix_links(filepath)

print("All links fixed!")

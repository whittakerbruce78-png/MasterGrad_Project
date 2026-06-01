import re
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_template():
    # search for the generic Vladivostok washing machines page
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files:
            path = os.path.join(root, 'index.html')
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '<h1 id="services-heading">Ремонт стиральных машин во Владивостоке на дому</h1>' in content or '<h1 id="services-heading">Ремонт стиральных машин во Владивостоке</h1>' in content:
                    # make sure it is not a district page
                    if 'район' not in path and 'raion' not in path.lower():
                        return content
    return None

template = get_template()
if not template:
    print("Could not find template")
    sys.exit(1)

def fix_city_page(city_folder, city_name_ru, city_map_file):
    dest_file = os.path.join(city_folder, 'index.html')
    
    content = template
    
    # Replace city names
    content = content.replace('Владивостоке', city_name_ru + 'е')
    content = content.replace('Владивосток', city_name_ru)
    content = content.replace('владивосток', city_name_ru.lower())
    content = content.replace('/стиральные-машины-иркутск/', '/irkutsk-stiralnie-mashini/')
    content = content.replace('/стиральные-машины-хабаровск/', '/khabarovsk-stiralnie-mashini/')
    
    # Replace map block
    with open(city_map_file, 'r', encoding='utf-8') as f:
        map_block = f.read()
    
    content = re.sub(r'<!-- БЛОК Карта.*?(\n.*?)?</section>', map_block, content, flags=re.DOTALL)
    
    # also fix the menu links if needed, but the template already has the right menu links structure probably, except maybe missing aria-current.
    
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {dest_file}")

fix_city_page('irkutsk-stiralnie-mashini', 'Иркутск', 'irk_map.txt')
fix_city_page('khabarovsk-stiralnie-mashini', 'Хабаровск', 'khv_map.txt')

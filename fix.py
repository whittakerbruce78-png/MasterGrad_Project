import re
import os
import base64
import sys

src_dir = base64.b64decode("0YHRgtC40YDQsNC70YzQvdGL0LUt0LzQsNGI0LjQvdGLLdCy0LvQsNC00LjQstC+0YHRgtC+0Lo=").decode('utf-8')
irk_ru = base64.b64decode("0JjRgNC60YPRgtGB0Lo=").decode('utf-8')
khv_ru = base64.b64decode("0KXQsNCx0LDRgNC+0LLRgdC6").decode('utf-8')
vld_ru = base64.b64decode("0JLQu9Cw0LTQuNCy0L7RgdGC0L7Qug==").decode('utf-8')
vlde_ru = base64.b64decode("0JLQu9Cw0LTQuNCy0L7RgdGC0L7QutC1").decode('utf-8')

print("Src dir:", repr(src_dir))

def fix_city_page(city_folder, city_name_ru, city_map_file, is_irkutsk):
    src_file = os.path.join(src_dir, 'index.html')
    dest_file = os.path.join(city_folder, 'index.html')
    
    with open(src_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace city names
    content = content.replace(vlde_ru, city_name_ru + 'е')
    content = content.replace(vld_ru, city_name_ru)
    content = content.replace(vld_ru.lower(), city_name_ru.lower())
    
    # fix links
    content = content.replace('/стиральные-машины-иркутск/', '/irkutsk-stiralnie-mashini/')
    content = content.replace('/стиральные-машины-хабаровск/', '/khabarovsk-stiralnie-mashini/')
    
    # Replace map block
    with open(city_map_file, 'r', encoding='utf-8') as f:
        map_block = f.read()
    
    content = re.sub(r'<!-- БЛОК Карта.*?(\n.*?)?</section>', map_block, content, flags=re.DOTALL)
    
    # Also update the title to match what they expect, the src title has "в Первомайском районе" because I'm using... wait, no, the root index.html of стиральные-машины-владивосток doesn't have "в Первомайском районе", it is the general washing machine page.
    
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {dest_file}")

fix_city_page('irkutsk-stiralnie-mashini', irk_ru, 'irk_map.txt', True)
fix_city_page('khabarovsk-stiralnie-mashini', khv_ru, 'khv_map.txt', False)

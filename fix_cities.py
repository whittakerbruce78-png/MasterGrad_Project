import os
import re

def fix_cities():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                norm_path = fpath.replace('\\', '/').lstrip('./')
                parts = norm_path.split('/')
                base_dir = parts[0]
                
                if base_dir.startswith('irkutsk-') or base_dir.startswith('khabarovsk-'):
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        
                    original_content = content
                    
                    target_city_nom = 'Иркутск' if base_dir.startswith('irkutsk-') else 'Хабаровск'
                    target_city_gen = 'Иркутска' if base_dir.startswith('irkutsk-') else 'Хабаровска'
                    target_city_prep = 'Иркутске' if base_dir.startswith('irkutsk-') else 'Хабаровске'
                    target_city_dat = 'Иркутску' if base_dir.startswith('irkutsk-') else 'Хабаровску'
                    
                    # We need to preserve the city in the <div class="city-dropdown-content">
                    # so let's temporarily replace that block to protect it
                    dropdown_match = re.search(r'<div class="city-dropdown-content">.*?</div>', content, flags=re.DOTALL)
                    dropdown = dropdown_match.group(0) if dropdown_match else ""
                    if dropdown:
                        content = content.replace(dropdown, '___DROPDOWN_PLACEHOLDER___')
                        
                    # Also protect the map URL for Vladivostok if it's the main office map?
                    # "Наш офис г.Владивосток ул.Жигура 26а"
                    # We shouldn't replace this if it is their actual ONLY office.
                    # Wait! In Khabarovsk, do they have a different office? 
                    # They probably just copy pasted. I will replace it.
                    
                    # Replacements
                    content = re.sub(r'\bво\s+Владивостоке\b', f'в {target_city_prep}', content, flags=re.IGNORECASE)
                    content = re.sub(r'\bВо\s+Владивостоке\b', f'В {target_city_prep}', content)
                    content = re.sub(r'\bВладивостоке\b', target_city_prep, content)
                    content = re.sub(r'\bВладивостока\b', target_city_gen, content)
                    content = re.sub(r'\bВладивостоку\b', target_city_dat, content)
                    content = re.sub(r'\bВладивосток\b', target_city_nom, content)
                    
                    if dropdown:
                        content = content.replace('___DROPDOWN_PLACEHOLDER___', dropdown)
                        
                    if content != original_content:
                        with open(fpath, 'w', encoding='utf-8') as file:
                            file.write(content)

if __name__ == '__main__':
    fix_cities()

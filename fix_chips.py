import os
import re

def fix_districts():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                original_content = content
                norm_path = fpath.replace('\\', '/').lstrip('./')
                parts = norm_path.split('/')
                base_dir = parts[0]
                
                if base_dir.startswith('irkutsk-'):
                    chips = f"""<div class="district-chips-list" style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
    <a href="/{base_dir}/pravoberezhniy-raion/" class="district-chip">Правобережный район</a>
    <a href="/{base_dir}/oktyabrskiy-raion/" class="district-chip">Октябрьский район</a>
    <a href="/{base_dir}/sverdlovskiy-raion/" class="district-chip">Свердловский район</a>
    <a href="/{base_dir}/leninskiy-raion/" class="district-chip">Ленинский район</a>
  </div>"""
                elif base_dir.startswith('khabarovsk-'):
                    chips = f"""<div class="district-chips-list" style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
    <a href="/{base_dir}/centralniy-raion/" class="district-chip">Центральный район</a>
    <a href="/{base_dir}/krasnoflotskiy-raion/" class="district-chip">Краснофлотский район</a>
    <a href="/{base_dir}/kirovskiy-raion/" class="district-chip">Кировский район</a>
    <a href="/{base_dir}/zheleznodorozhniy-raion/" class="district-chip">Железнодорожный район</a>
    <a href="/{base_dir}/industrialniy-raion/" class="district-chip">Индустриальный район</a>
  </div>"""
                elif base_dir in ['стиральные-машины-владивосток', 'холодильники-владивосток', 'водонагреватели-владивосток', 'посудомоечные-машины-владивосток']:
                    chips = f"""<div class="district-chips-list" style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
    <a href="/{base_dir}/ленинский-район/" class="district-chip">Ленинский район</a>
    <a href="/{base_dir}/первомайский-район/" class="district-chip">Первомайский район</a>
    <a href="/{base_dir}/первореченский-район/" class="district-chip">Первореченский район</a>
    <a href="/{base_dir}/советский-район/" class="district-chip">Советский район</a>
    <a href="/{base_dir}/фрунзенский-район/" class="district-chip">Фрунзенский район</a>
  </div>"""
                else:
                    continue
                    
                content = re.sub(r'<div class="district-chips-list".*?</div>', chips, content, flags=re.DOTALL)
                
                if content != original_content:
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(content)

if __name__ == '__main__':
    fix_districts()

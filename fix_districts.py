import os
import re

def fix_districts():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                norm_path = fpath.replace('\\', '/').lstrip('./')
                parts = norm_path.split('/')
                base_dir = parts[0]
                
                if base_dir.startswith('irkutsk-'):
                    districts = f"""<section class="districts">
    <div class="container">
        <h2>Районы обслуживания</h2>
        <div class="district-links">
            <a href="/{base_dir}/pravoberezhniy-raion/">Правобережный район</a>
            <a href="/{base_dir}/oktyabrskiy-raion/">Октябрьский район</a>
            <a href="/{base_dir}/sverdlovskiy-raion/">Свердловский район</a>
            <a href="/{base_dir}/leninskiy-raion/">Ленинский район</a>
        </div>
    </div>
</section>"""
                elif base_dir.startswith('khabarovsk-'):
                    districts = f"""<section class="districts">
    <div class="container">
        <h2>Районы обслуживания</h2>
        <div class="district-links">
            <a href="/{base_dir}/centralniy-raion/">Центральный район</a>
            <a href="/{base_dir}/krasnoflotskiy-raion/">Краснофлотский район</a>
            <a href="/{base_dir}/kirovskiy-raion/">Кировский район</a>
            <a href="/{base_dir}/zheleznodorozhniy-raion/">Железнодорожный район</a>
            <a href="/{base_dir}/industrialniy-raion/">Индустриальный район</a>
        </div>
    </div>
</section>"""
                elif base_dir in ['стиральные-машины-владивосток', 'холодильники-владивосток', 'водонагреватели-владивосток', 'посудомоечные-машины-владивосток']:
                    districts = f"""<section class="districts">
    <div class="container">
        <h2>Районы обслуживания</h2>
        <div class="district-links">
            <a href="/{base_dir}/ленинский-район/">Ленинский район</a>
            <a href="/{base_dir}/первомайский-район/">Первомайский район</a>
            <a href="/{base_dir}/первореченский-район/">Первореченский район</a>
            <a href="/{base_dir}/советский-район/">Советский район</a>
            <a href="/{base_dir}/фрунзенский-район/">Фрунзенский район</a>
        </div>
    </div>
</section>"""
                else:
                    continue
                    
                new_content = re.sub(r'<section class="districts">.*?</section>', districts, content, flags=re.DOTALL)
                
                if new_content != content:
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(new_content)

if __name__ == '__main__':
    fix_districts()

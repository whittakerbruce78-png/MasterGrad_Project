import os
import re

districts_by_city = {
    'vladivostok': [
        ('leninskiy-raion', 'Ленинский район'),
        ('pervorechenskiy-raion', 'Первореченский район'),
        ('sovetskiy-raion', 'Советский район'),
        ('pervomaiskiy-raion', 'Первомайский район'),
        ('frunzenskiy-raion', 'Фрунзенский район')
    ],
    'khabarovsk': [
        ('centralniy-raion', 'Центральный район'),
        ('industrialniy-raion', 'Индустриальный район'),
        ('kirovskiy-raion', 'Кировский район'),
        ('krasnoflotskiy-raion', 'Краснофлотский район'),
        ('zheleznodorozhniy-raion', 'Железнодорожный район')
    ],
    'irkutsk': [
        ('pravoberezhniy-raion', 'Правобережный район'),
        ('oktyabrskiy-raion', 'Октябрьский район'),
        ('sverdlovskiy-raion', 'Свердловский район'),
        ('leninskiy-raion', 'Ленинский район')
    ]
}

# Determine city from path
def get_city(rel_path):
    parts = rel_path.split(os.sep)
    for p in parts:
        if 'vladivostok' in p:
            return 'vladivostok'
        if 'khabarovsk' in p:
            return 'khabarovsk'
        if 'irkutsk' in p:
            return 'irkutsk'
    # Default to vladivostok for root files
    return 'vladivostok'

project_root = os.getcwd()
html_files = []
for root, dirs, files in os.walk(project_root):
    if '.git' in root.split(os.sep):
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.php'):
            html_files.append(os.path.join(root, f))

for fpath in html_files:
    rel_path = os.path.relpath(fpath, project_root)
    parts = rel_path.split(os.sep)
    file_depth = len(parts) - 1
    
    # We only care about city-specific category files (depth 1) and district files (depth 2)
    city = get_city(rel_path)
    dist_list = districts_by_city.get(city, [])
    
    # Calculate rel_prefix to parent category folder
    # For depth 1 (e.g. vladivostok-stiralnie-mashini/index.html):
    #   links to districts should be ./<district>/
    # For depth 2 (e.g. vladivostok-stiralnie-mashini/leninskiy-raion/index.html):
    #   links to districts should be ../<district>/
    rel_prefix = '../' if file_depth == 2 else './'
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    original_content = content
    
    # 1. Replace the district-chips-list block
    # Generate new chips HTML
    chips_html = '\n'.join([
        f'<a class="district-chip" href="{rel_prefix}{d_id}/">{d_name}</a>'
        for d_id, d_name in dist_list
    ])
    
    # Regex to find <div class="district-chips-list" ...> ... </div>
    pattern_chips = r'(<div class="district-chips-list"[^>]*>)(.*?)(</div>)'
    def replace_chips(match):
        return f"{match.group(1)}\n{chips_html}\n{match.group(3)}"
        
    content = re.sub(pattern_chips, replace_chips, content, flags=re.DOTALL)
    
    # 2. Replace the district links in the SEO text paragraph
    # Let's find: Ремонтируем на дому во всех районах ... Выезжаем быстро и бесплатно: ...
    # We want to replace all links inside that paragraph with correct ones
    # E.g. <p>Ремонтируем на дому во всех районах ... Выезжаем быстро и бесплатно: <links> а также ... </p>
    pattern_seo = r'(Ремонтируем на дому во всех районах [^<]*Выезжаем быстро и бесплатно:)(.*?)(а также|•|$)'
    
    seo_links_html = ' ' + ', '.join([
        f'<a href="{rel_prefix}{d_id}/">{d_name}</a>'
        for d_id, d_name in dist_list
    ]) + ', '
    
    def replace_seo(match):
        return f"{match.group(1)}{seo_links_html}{match.group(3)}"
        
    content = re.sub(pattern_seo, replace_seo, content, flags=re.DOTALL | re.IGNORECASE)
    
    # 3. Specifically fix spasibo/index.html unused services
    if 'spasibo' in rel_path:
        # Comment out the unused services in "Мы ремонтируем всю технику"
        # Let's find repair items starting with Кондиционеры, Плиты, Духовые шкафы, Телевизоры, Малая бытовая техника, Компьютеры
        # E.g. <a aria-label="Ремонт кондиционеров" ...> ... </a>
        # We can comment out items with t5.png, t6.png, t7.png, t8.png, t9.png, t10.png
        # Let's see: in spasibo/index.html, they were:
        # <a aria-label="Ремонт кондиционеров" ...> ... </a>
        # Let's match each and comment it out or delete it to make it clean
        for num in range(5, 11):
            pattern_item = rf'(<a[^>]*class="repair-item[^>]*href="[^"]*(?:кондиционеры|плиты|духовые|телевизоры|компьютеры|малая)[^"]*"[^>]*>.*?</a>)'
            content = re.sub(pattern_item, r'<!-- \1 -->', content, flags=re.DOTALL)
            
            # Also handle if it links to relative paths with t5.png to t10.png
            pattern_img_item = rf'(<a[^>]*class="repair-item[^>]*>.*?img/t{num}\.png.*?</a>)'
            content = re.sub(pattern_img_item, r'<!-- \1 -->', content, flags=re.DOTALL)

    if content != original_content:
        print(f"Updated district links/chips in: {rel_path}")
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print("District links fix complete.")

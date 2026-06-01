import os
import re

def process_all():
    # 1. Gather all files
    all_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                all_files.append(os.path.join(root, f))
                
    files_modified = 0
    
    for fpath in all_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Determine city based on folder path
        norm_path = fpath.replace('\\', '/')
        if 'irkutsk-' in norm_path:
            city = 'irkutsk'
        elif 'khabarovsk-' in norm_path:
            city = 'khabarovsk'
        else:
            city = 'vladivostok'
            
        # Fix nav links
        if city == 'irkutsk':
            # We want to replace the hrefs inside the nav sidebar
            # The structure is usually <li><a href="...">Text</a></li>
            # But the hrefs might be totally wrong.
            # We will use regex to find the links by their text content, because text is consistent!
            
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Стиральные машины|Ремонт стиральных машин)</a>', r'<a href="/irkutsk-stiralnie-mashini/">\1</a>', content)
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Холодильники|Ремонт холодильников)</a>', r'<a href="/irkutsk-holodilniki/">\1</a>', content)
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Водонагреватели|Ремонт водонагревателей)</a>', r'<a href="/irkutsk-vodonagrevateli/">\1</a>', content)
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Посудомоечные машины|Ремонт посудомоечных машин)</a>', r'<a href="/irkutsk-posudomoechnie-mashini/">\1</a>', content)
            
        elif city == 'khabarovsk':
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Стиральные машины|Ремонт стиральных машин)</a>', r'<a href="/khabarovsk-stiralnie-mashini/">\1</a>', content)
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Холодильники|Ремонт холодильников)</a>', r'<a href="/khabarovsk-holodilniki/">\1</a>', content)
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Водонагреватели|Ремонт водонагревателей)</a>', r'<a href="/khabarovsk-vodonagrevateli/">\1</a>', content)
            content = re.sub(r'<a[^>]*href=["\'][^"\']+["\'][^>]*>(Посудомоечные машины|Ремонт посудомоечных машин)</a>', r'<a href="/khabarovsk-posudomoechnie-mashini/">\1</a>', content)

        # Fix district links in my mistakenly overwritten files
        if 'irkutsk-stiralnie-mashini/index.html' in norm_path or 'irkutsk-stiralnie-mashini\\index.html' in norm_path:
            # Rebuild district section for Irkutsk
            irk_districts = """<section class="districts">
    <div class="container">
        <h2>Районы обслуживания</h2>
        <div class="district-links">
            <a href="/irkutsk-stiralnie-mashini/pravoberezhniy-raion/">Правобережный район</a>
            <a href="/irkutsk-stiralnie-mashini/oktyabrskiy-raion/">Октябрьский район</a>
            <a href="/irkutsk-stiralnie-mashini/sverdlovskiy-raion/">Свердловский район</a>
            <a href="/irkutsk-stiralnie-mashini/leninskiy-raion/">Ленинский район</a>
        </div>
    </div>
</section>"""
            content = re.sub(r'<section class="districts">.*?</section>', irk_districts, content, flags=re.DOTALL)

        if 'khabarovsk-stiralnie-mashini/index.html' in norm_path or 'khabarovsk-stiralnie-mashini\\index.html' in norm_path:
            # Rebuild district section for Khabarovsk
            khv_districts = """<section class="districts">
    <div class="container">
        <h2>Районы обслуживания</h2>
        <div class="district-links">
            <a href="/khabarovsk-stiralnie-mashini/centralniy-raion/">Центральный район</a>
            <a href="/khabarovsk-stiralnie-mashini/krasnoflotskiy-raion/">Краснофлотский район</a>
            <a href="/khabarovsk-stiralnie-mashini/kirovskiy-raion/">Кировский район</a>
            <a href="/khabarovsk-stiralnie-mashini/zheleznodorozhniy-raion/">Железнодорожный район</a>
            <a href="/khabarovsk-stiralnie-mashini/industrialniy-raion/">Индустриальный район</a>
        </div>
    </div>
</section>"""
            content = re.sub(r'<section class="districts">.*?</section>', khv_districts, content, flags=re.DOTALL)
            
        if content != original_content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            files_modified += 1
            
    print(f"Fixed {files_modified} files.")

if __name__ == '__main__':
    process_all()

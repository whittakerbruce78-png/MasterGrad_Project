import os
from bs4 import BeautifulSoup

def fix_seo():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                soup = BeautifulSoup(content, 'html.parser')
                changed = False
                
                # Fix Images
                for img in soup.find_all('img'):
                    if not img.get('alt') or str(img.get('alt')).strip() == '':
                        img['alt'] = "Ремонт бытовой техники МастерГрад"
                        changed = True

                # Fix Title
                title_tag = soup.find('title')
                h1_tag = soup.find('h1')
                default_title = h1_tag.text.strip() if h1_tag else "МастерГрад — ремонт бытовой техники"
                
                if not title_tag:
                    head = soup.find('head')
                    if head:
                        new_title = soup.new_tag('title')
                        new_title.string = default_title
                        head.append(new_title)
                        changed = True
                elif not title_tag.text.strip():
                    title_tag.string = default_title
                    changed = True

                # Fix Description
                desc_tag = soup.find('meta', attrs={'name': 'description'})
                default_desc = "Профессиональный ремонт бытовой техники на дому. Быстрый выезд мастера, оригинальные запчасти, гарантия качества."
                
                if not desc_tag:
                    head = soup.find('head')
                    if head:
                        new_meta = soup.new_tag('meta')
                        new_meta['name'] = 'description'
                        new_meta['content'] = default_desc
                        head.append(new_meta)
                        changed = True
                elif not desc_tag.get('content', '').strip():
                    desc_tag['content'] = default_desc
                    changed = True

                if changed:
                    # using HTML5 formatter to avoid breaking existing syntax
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(str(soup))

if __name__ == '__main__':
    fix_seo()

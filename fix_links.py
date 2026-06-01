import os
import re

mapping = {
    '/холодильники-иркутск/': '/irkutsk-holodilniki/',
    '/посудомоечные-машины-иркутск/': '/irkutsk-posudomoechnie-mashini/',
    '/стиральные-машины-иркутск/': '/irkutsk-stiralnie-mashini/',
    '/водонагреватели-иркутск/': '/irkutsk-vodonagrevateli/',
    '/холодильники-хабаровск/': '/khabarovsk-holodilniki/',
    '/посудомоечные-машины-хабаровск/': '/khabarovsk-posudomoechnie-mashini/',
    '/стиральные-машины-хабаровск/': '/khabarovsk-stiralnie-mashini/',
    '/водонагреватели-хабаровск/': '/khabarovsk-vodonagrevateli/',
}

# Also handle without trailing slash just in case
mapping_no_slash = {k[:-1]: v[:-1] for k, v in mapping.items()}

def fix_all_links():
    root_dir = '.'
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    files_changed = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        for ru, lat in mapping.items():
            content = content.replace(ru, lat)
            
        # specifically inside hrefs to avoid replacing text
        for ru, lat in mapping_no_slash.items():
            content = content.replace(f'href="{ru}"', f'href="{lat}"')
            content = content.replace(f"href='{ru}'", f"href='{lat}'")
            # in case they have hash fragments or queries
            content = re.sub(f'href="{ru}(#|\\?|/)', f'href="{lat}\\1', content)
            
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            files_changed += 1

    print(f"Fixed links in {files_changed} files.")

if __name__ == "__main__":
    fix_all_links()

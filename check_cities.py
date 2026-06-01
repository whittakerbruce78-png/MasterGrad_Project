import os
import re

def check_cities():
    issues = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                # We expect Khabarovsk pages to NOT contain "Иркутск" outside of the menu
                # We expect Irkutsk pages to NOT contain "Хабаровск" outside of the menu
                # We expect Vladivostok pages to NOT contain "Иркутск" or "Хабаровск" outside of the menu
                
                # strip out the header/menu which legit has "Иркутск" and "Хабаровск"
                # The menu is roughly from <header class="site-header"> to </header>
                content_no_header = re.sub(r'<header class="site-header">.*?</header>', '', content, flags=re.DOTALL)
                
                norm_path = fpath.replace('\\', '/').lstrip('./')
                parts = norm_path.split('/')
                base_dir = parts[0]
                
                if base_dir.startswith('khabarovsk-'):
                    # if it has "Иркутск" or "Владивосток"
                    if 'Иркутск' in content_no_header:
                        issues.append(f"{fpath} contains 'Иркутск'")
                    if 'Владивосток' in content_no_header:
                        issues.append(f"{fpath} contains 'Владивосток'")
                elif base_dir.startswith('irkutsk-'):
                    if 'Хабаровск' in content_no_header:
                        issues.append(f"{fpath} contains 'Хабаровск'")
                    if 'Владивосток' in content_no_header:
                        issues.append(f"{fpath} contains 'Владивосток'")
                elif base_dir in ['стиральные-машины-владивосток', 'холодильники-владивосток', 'водонагреватели-владивосток', 'посудомоечные-машины-владивосток']:
                    if 'Хабаровск' in content_no_header:
                        issues.append(f"{fpath} contains 'Хабаровск'")
                    if 'Иркутск' in content_no_header:
                        issues.append(f"{fpath} contains 'Иркутск'")
                        
    with open('city_issues.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(issues))

if __name__ == '__main__':
    check_cities()

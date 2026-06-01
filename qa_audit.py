import os
import re
from bs4 import BeautifulSoup
from collections import defaultdict

def run_qa_audit():
    stats = {
        'total_pages': 0,
        'missing_title': [],
        'missing_desc': [],
        'missing_h1': [],
        'multiple_h1': [],
        'broken_images': [],
        'missing_alt': [],
        'lorem_ipsum': [],
        'forms_without_required': [],
        'empty_links': []
    }
    
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                stats['total_pages'] += 1
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # SEO & Technical
                    title = soup.find('title')
                    if not title or not title.text.strip():
                        stats['missing_title'].append(fpath)
                        
                    desc = soup.find('meta', attrs={'name': 'description'})
                    if not desc or not desc.get('content', '').strip():
                        stats['missing_desc'].append(fpath)
                        
                    h1_tags = soup.find_all('h1')
                    if len(h1_tags) == 0:
                        stats['missing_h1'].append(fpath)
                    elif len(h1_tags) > 1:
                        stats['multiple_h1'].append(fpath)
                        
                    # Images
                    images = soup.find_all('img')
                    for img in images:
                        src = img.get('src', '')
                        alt = img.get('alt')
                        if not src:
                            pass # inline or lazy
                        elif not src.startswith('http') and not src.startswith('data:'):
                            # check if local file exists
                            # src can be ../img/something.png
                            # let's assume it's somewhat valid but check for alt
                            pass
                        
                        if alt is None or alt.strip() == '':
                            # It's not necessarily broken but it's missing alt
                            # We just count one per file to not clutter
                            if fpath not in stats['missing_alt']:
                                stats['missing_alt'].append(fpath)

                    # Links
                    links = soup.find_all('a')
                    for a in links:
                        href = a.get('href')
                        if not href or href.strip() == '' or href == '#':
                            if fpath not in stats['empty_links']:
                                stats['empty_links'].append(fpath)

                    # Content
                    if 'lorem ipsum' in content.lower():
                        stats['lorem_ipsum'].append(fpath)

                    # Forms
                    forms = soup.find_all('form')
                    for form in forms:
                        inputs = form.find_all(['input', 'textarea', 'select'])
                        has_required = any(inp.has_attr('required') for inp in inputs)
                        if not has_required:
                            stats['forms_without_required'].append(fpath)

                except Exception as e:
                    print(f"Error parsing {fpath}: {e}")

    with open('qa_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total Pages: {stats['total_pages']}\n")
        f.write(f"Missing Title: {len(stats['missing_title'])}\n")
        f.write(f"Missing Desc: {len(stats['missing_desc'])}\n")
        f.write(f"Missing H1: {len(stats['missing_h1'])}\n")
        f.write(f"Multiple H1: {len(stats['multiple_h1'])}\n")
        f.write(f"Missing Alt Text: {len(stats['missing_alt'])}\n")
        f.write(f"Empty Links (# or empty): {len(stats['empty_links'])}\n")
        f.write(f"Lorem Ipsum: {len(stats['lorem_ipsum'])}\n")
        f.write(f"Forms without required fields: {len(stats['forms_without_required'])}\n")
        
if __name__ == '__main__':
    run_qa_audit()

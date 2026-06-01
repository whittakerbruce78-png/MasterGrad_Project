import os
import re
from urllib.parse import urlparse, unquote

def check_all_links():
    root_dir = '.'
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    broken_links = set()
    total_links = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        hrefs = re.findall(r'href=[\'"]?([^\'" >]+)', content)
        
        for href in hrefs:
            total_links += 1
            if href.startswith('http://') or href.startswith('https://') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            if href.startswith('#'):
                continue
                
            decoded_href = unquote(href)
            if '#' in decoded_href:
                decoded_href = decoded_href.split('#')[0]
                
            if decoded_href.startswith('/'):
                target_path = os.path.join(root_dir, decoded_href.lstrip('/'))
            else:
                target_path = os.path.join(os.path.dirname(html_file), decoded_href)
                
            target_path = os.path.normpath(target_path)
            
            if os.path.isdir(target_path):
                target_path = os.path.join(target_path, 'index.html')
                
            if not os.path.exists(target_path):
                if not os.path.exists(os.path.dirname(target_path)):
                    broken_links.add((html_file, href))
                else:
                    broken_links.add((html_file, href))

    with open('broken_links.txt', 'w', encoding='utf-8') as out:
        out.write(f"Total HTML files checked: {len(html_files)}\n")
        out.write(f"Total internal links checked: {total_links}\n")
        out.write(f"Total unique broken links found: {len(broken_links)}\n\n")
        out.write("--- BROKEN LINKS SUMMARY ---\n")
        
        link_sources = {}
        for source_file, link in broken_links:
            if link not in link_sources:
                link_sources[link] = []
            link_sources[link].append(source_file)
            
        for link, sources in sorted(link_sources.items()):
            out.write(f"Broken Link: {link} (Found in {len(sources)} files)\n")
            for source in sources[:3]:
                out.write(f"  - in {source}\n")
            if len(sources) > 3:
                out.write(f"  ... and {len(sources) - 3} more\n")
            out.write("\n")

if __name__ == "__main__":
    check_all_links()

import os
import re
import urllib.parse

# 1. Directory Mapping
dir_map = {
    # Russian folder names
    'стиральные-машины-владивосток': 'vladivostok-stiralnie-mashini',
    'холодильники-владивосток': 'vladivostok-holodilniki',
    'водонагреватели-владивосток': 'vladivostok-vodonagrevateli',
    'посудомоечные-машины-владивосток': 'vladivostok-posudomoechnie-mashini',
    'спасибо': 'spasibo',
    # Districts
    'ленинский-район': 'leninskiy-raion',
    'первомайский-район': 'pervomaiskiy-raion',
    'первореченский-район': 'pervorechenskiy-raion',
    'советский-район': 'sovetskiy-raion',
    'фрунзенский-район': 'frunzenskiy-raion'
}

# Expand dir_map to include all corrupted / encoded variations
expanded_map = {}
for k, v in dir_map.items():
    expanded_map[k] = v
    # lowercase URL-encoded
    enc_k_lower = urllib.parse.quote(k).lower()
    expanded_map[enc_k_lower] = v
    # uppercase URL-encoded
    enc_k_upper = urllib.parse.quote(k).upper()
    expanded_map[enc_k_upper] = v
    # cp1251 decoded from utf-8
    try:
        corrupted_1 = k.encode('utf-8').decode('cp1251')
        expanded_map[corrupted_1] = v
        expanded_map[urllib.parse.quote(corrupted_1).lower()] = v
        expanded_map[urllib.parse.quote(corrupted_1).upper()] = v
    except: pass
    # utf-8 decoded from cp1251
    try:
        corrupted_2 = k.encode('cp1251').decode('utf-8')
        expanded_map[corrupted_2] = v
        expanded_map[urllib.parse.quote(corrupted_2).lower()] = v
        expanded_map[urllib.parse.quote(corrupted_2).upper()] = v
    except: pass

# Also let's sort key by length descending to avoid substring issues
sorted_keys = sorted(expanded_map.keys(), key=len, reverse=True)

def replace_city_folders(content):
    # Replace all occurrences of these folder names in the text/html
    for key in sorted_keys:
        val = expanded_map[key]
        content = content.replace(key, val)
    return content

def fix_attrib(match, file_depth):
    attr = match.group(1) # e.g. href, src, action
    quote = match.group(2) # e.g. ", '
    path = match.group(3) # the actual path
    
    # If path starts with http/https/tel/mailto or #, don't modify it
    if path.startswith(('http://', 'https://', 'tel:', 'mailto:', '#', 'javascript:')):
        return match.group(0)
        
    rel_prefix = '../' * file_depth if file_depth > 0 else './'
    
    # Clean up MasterGrad_Project prefix
    if path.startswith('/MasterGrad_Project/'):
        path = path[len('/MasterGrad_Project/'):]
    elif path.startswith('/MasterGrad_Project'):
        path = path[len('/MasterGrad_Project'):].lstrip('/')
        
    # Clean up leading slash
    if path.startswith('/'):
        path = path.lstrip('/')
        
    # Clean up `./` or `../` if they already exist, so we reconstruct clean relative path
    # E.g. if path is `./css/style.css`, we want just `css/style.css`
    while path.startswith('./'):
        path = path[2:]
    while path.startswith('../'):
        path = path[3:]
        
    new_path = rel_prefix + path
    return f'{attr}={quote}{new_path}{quote}'

def fix_fetch_or_url(match, file_depth):
    func = match.group(1) # e.g. fetch, url
    quote = match.group(2) if match.group(2) else '' # e.g. ", ', or empty
    path = match.group(3) # the actual path
    
    # If path starts with http/https or # or data:, don't modify it
    if path.startswith(('http://', 'https://', '#', 'data:')):
        return match.group(0)
        
    rel_prefix = '../' * file_depth if file_depth > 0 else './'
    
    # Clean up MasterGrad_Project prefix
    if path.startswith('/MasterGrad_Project/'):
        path = path[len('/MasterGrad_Project/'):]
    elif path.startswith('/MasterGrad_Project'):
        path = path[len('/MasterGrad_Project'):].lstrip('/')
        
    # Clean up leading slash
    if path.startswith('/'):
        path = path.lstrip('/')
        
    while path.startswith('./'):
        path = path[2:]
    while path.startswith('../'):
        path = path[3:]
        
    new_path = rel_prefix + path
    
    if func.startswith('url'):
        return f'{func}({quote}{new_path}{quote})'
    else:
        return f'{func}({quote}{new_path}{quote})'

# Walk all HTML files
project_root = os.getcwd()
html_files = []
for root, dirs, files in os.walk(project_root):
    # Skip .git directories
    if '.git' in root.split(os.sep):
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.php'):
            html_files.append(os.path.join(root, f))

print(f"Found {len(html_files)} HTML/PHP files.")

for fpath in html_files:
    # Calculate depth relative to project root
    rel_path = os.path.relpath(fpath, project_root)
    # depth is the number of directories
    parts = rel_path.split(os.sep)
    file_depth = len(parts) - 1
    
    # Skip original.html if we want, but let's process it too
    print(f"Processing: {rel_path} (depth={file_depth})")
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Apply folder mapping to rename Vladivostok Cyrillic/corrupted links
    content = replace_city_folders(content)
    
    # Make attributes relative: href="..." src="..." action="..."
    content = re.sub(
        r'(href|src|action)\s*=\s*(["\'])([^"\']+)\2',
        lambda m: fix_attrib(m, file_depth),
        content,
        flags=re.IGNORECASE
    )
    
    # Make fetch('...') or fetch("...") and url('...') or url("...") relative
    content = re.sub(
        r'(fetch|url)\s*\(\s*(["\']?)([^"\'\)]+)\2\s*\)',
        lambda m: fix_fetch_or_url(m, file_depth),
        content,
        flags=re.IGNORECASE
    )
    
    # Fix canonical tags specifically to be correct absolute URLs
    # Wait, canonical link tag shouldn't be made relative! It MUST be absolute for SEO.
    # E.g. <link href="https://мастер-град.рф/vladivostok-stiralnie-mashini/" rel="canonical"/>
    # Let's fix if canonical tag got corrupted/made relative.
    # Since canonical starts with https://, our fix_attrib ignored it, which is perfect!
    # But wait, did it contain Cyrillic folder names?
    # Yes, e.g. <link href="https://мастер-град.рф/стиральные-машины-владивосток/" rel="canonical"/>
    # replace_city_folders replaced it to `https://мастер-град.рф/vladivostok-stiralnie-mashini/`, which is perfect!
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update sitemap.xml to use English paths instead of Cyrillic/corrupted
sitemap_path = os.path.join(project_root, 'sitemap.xml')
if os.path.exists(sitemap_path):
    print("Updating sitemap.xml...")
    with open(sitemap_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    content = replace_city_folders(content)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fix completed successfully!")

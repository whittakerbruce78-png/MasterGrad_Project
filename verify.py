import os
import re
import urllib.parse

html_files = []
project_root = os.getcwd()

for root, dirs, files in os.walk(project_root):
    if '.git' in root.split(os.sep):
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.php'):
            html_files.append(os.path.join(root, f))

print(f"Verifying {len(html_files)} HTML/PHP files...")

broken_links = []
absolute_remnants = []
cyrillic_remnants = []

# List of Cyrillic/corrupted segments to watch out for
cyrillic_watch = [
    'стиральные-машины-владивосток',
    'холодильники-владивосток',
    'водонагреватели-владивосток',
    'посудомоечные-машины-владивосток',
    'ленинский-район',
    'первомайский-район',
    'первореченский-район',
    'советский-район',
    'фрунзенский-район',
    'спасибо'
]

# Add corrupted forms
cyrillic_corrupted = [
    'РІРѕРґРѕРЅР°РіСЂРµРІР°С‚РµР»Рё-РІР»Р°РґРёРІРѕСЃС‚РѕРє',
    'РїРѕСЃСѓРґРѕРјРѕРµС‡РЅС‹Рµ-РјР°С€РёРЅС‹-РІР»Р°РґРёРІРѕСЃС‚РѕРє',
    'СЃС‚РёСЂР°Р»СЊРЅС‹Рµ-РјР°С€РёРЅС‹-РІР»Р°РґРёРІРѕСЃС‚РѕРє',
    'С…РѕР»РѕРґРёР»СЊРЅРёРєРё-РІР»Р°РґРёРІРѕСЃС‚РѕРє',
    'СЃРїР°СЃРёР±Рѕ',
    'Р»РµРЅРёРЅСЃРєРёР№-СЂР°Р№РѕРЅ',
    'РїРµСЂРІРѕРјР°Р№СЃРєРёР№-СЂР°Р№РѕРЅ',
    'РїРµСЂРІРѕСЂРµС‡РµРЅСЃРєРёР№-СЂР°Р№РѕРЅ',
    'СЃРѕРІРµС‚СЃРєРёР№-СЂР°Р№РѕРЅ',
    'С„СЂСѓРЅР·РµРЅСЃРєРёР№-СЂР°Р№РѕРЅ'
]

watch_list = cyrillic_watch + cyrillic_corrupted

for fpath in html_files:
    rel_path = os.path.relpath(fpath, project_root)
    file_dir = os.path.dirname(fpath)
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Check for Cyrillic/corrupted links
    for item in watch_list:
        # Check if it exists in href/src attribute or fetch/url calls
        if item in content:
            # Check if it is a canonical link, which is allowed to be cyrillic for SEO
            # E.g. <link href="https://мастер-град.рф/...
            # Let's find occurrences of item in content that are NOT part of the cyrillic domain
            occurrences = [m.start() for m in re.finditer(re.escape(item), content)]
            for occ in occurrences:
                # Look at preceding context of 100 characters to check if it's the domain canonical tag
                context = content[max(0, occ-100):occ]
                if 'мастер-град.рф' not in context and 'xn----7sbblgc1c8acfl' not in context:
                    cyrillic_remnants.append((rel_path, item, content[max(0, occ-40):occ+40].strip()))
                    break

    # Extract all href and src paths
    links = re.findall(r'(href|src|action)\s*=\s*(["\'])([^"\']+)\2', content, flags=re.IGNORECASE)
    
    for attr, quote, target in links:
        # Check for absolute path remnants (starting with /MasterGrad_Project/ or /)
        if target.startswith('/MasterGrad_Project') or (target.startswith('/') and not target.startswith('//')):
            # Special check: /script/data.json or /css/ etc.
            # But let's log any absolute paths
            absolute_remnants.append((rel_path, f"{attr}={quote}{target}{quote}"))
            continue
            
        # Ignore external links, mailto, tel, anchor tags
        if target.startswith(('http://', 'https://', 'tel:', 'mailto:', '#', 'javascript:')):
            continue
            
        # URL decode target path
        decoded_target = urllib.parse.unquote(target)
        
        # Split target into path and optional query/anchor
        target_clean = decoded_target.split('?')[0].split('#')[0]
        if not target_clean or target_clean == './' or target_clean == '../':
            continue
            
        # Compute absolute filepath of target link
        target_abs_path = os.path.normpath(os.path.join(file_dir, target_clean))
        
        # Verify existence
        if not os.path.exists(target_abs_path):
            broken_links.append((rel_path, f"{attr}={quote}{target}{quote} (resolves to: {os.path.relpath(target_abs_path, project_root)})"))

print("\n--- RESULTS ---")

if absolute_remnants:
    print(f"\n[!] Absolute Path Remnants Found ({len(absolute_remnants)}):")
    for file, rem in absolute_remnants[:20]:
        print(f"  {file}: {rem}")
    if len(absolute_remnants) > 20:
        print(f"  ... and {len(absolute_remnants) - 20} more.")
else:
    print("\n[+] No absolute path remnants found!")

if cyrillic_remnants:
    print(f"\n[!] Cyrillic/Corrupted Remnants Found ({len(cyrillic_remnants)}):")
    for file, item, context in cyrillic_remnants[:20]:
        print(f"  {file}: Found '{item}' in context: ... {context} ...")
    if len(cyrillic_remnants) > 20:
        print(f"  ... and {len(cyrillic_remnants) - 20} more.")
else:
    print("\n[+] No Cyrillic/corrupted remnants found!")

if broken_links:
    print(f"\n[!] Broken Relative Links Found ({len(broken_links)}):")
    for file, link in broken_links[:20]:
        print(f"  {file}: {link}")
    if len(broken_links) > 20:
        print(f"  ... and {len(broken_links) - 20} more.")
else:
    print("\n[+] All relative links resolve to existing files successfully!")

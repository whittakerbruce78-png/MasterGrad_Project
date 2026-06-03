import os
import re

# Main service folders mapping
main_folders_mapping = {
    'vladivostok-stiralnie-mashini': 'стиральные-машины-владивосток',
    'vladivostok-holodilniki': 'холодильники-владивосток',
    'vladivostok-vodonagrevateli': 'водонагреватели-владивосток',
    'vladivostok-posudomoechnie-mashini': 'посудомоечные-машины-владивосток',
    'irkutsk-stiralnie-mashini': 'стиральные-машины-иркутск',
    'irkutsk-holodilniki': 'холодильники-иркутск',
    'irkutsk-vodonagrevateli': 'водонагреватели-иркутск',
    'irkutsk-posudomoechnie-mashini': 'посудомоечные-машины-иркутск',
    'khabarovsk-stiralnie-mashini': 'стиральные-машины-хабаровск',
    'khabarovsk-holodilniki': 'холодильники-хабаровск',
    'khabarovsk-vodonagrevateli': 'водонагреватели-хабаровск',
    'khabarovsk-posudomoechnie-mashini': 'посудомоечные-машины-хабаровск',
}

# District folders mapping
district_folders_mapping = {
    'leninskiy-raion': 'ленинский-район',
    'pervomaiskiy-raion': 'первомайский-район',
    'pervorechenskiy-raion': 'первореченский-район',
    'sovetskiy-raion': 'советский-район',
    'frunzenskiy-raion': 'фрунзенский-район',
    'oktyabrskiy-raion': 'октябрьский-район',
    'pravoberezhniy-raion': 'правобережный-район',
    'sverdlovskiy-raion': 'свердловский-район',
    'centralniy-raion': 'центральный-район',
    'industrialniy-raion': 'индустриальный-район',
    'kirovskiy-raion': 'кировский-район',
    'krasnoflotskiy-raion': 'краснофлотский-район',
    'zheleznodorozhniy-raion': 'железнодорожный-район',
}

def rename_folders():
    print("=== Step 1: Renaming subfolders (districts) ===")
    for old_main, new_main in main_folders_mapping.items():
        if os.path.exists(old_main):
            print(f"Entering service folder: {old_main}")
            # Scan subdirectories inside
            for sub in os.listdir(old_main):
                sub_path = os.path.join(old_main, sub)
                if os.path.isdir(sub_path):
                    if sub in district_folders_mapping:
                        new_sub = district_folders_mapping[sub]
                        new_sub_path = os.path.join(old_main, new_sub)
                        print(f"  Renaming district folder: {sub_path} -> {new_sub_path}")
                        os.rename(sub_path, new_sub_path)
                    else:
                        print(f"  Unknown subdirectory (skipping): {sub_path}")

    print("\n=== Step 2: Renaming main service folders ===")
    for old_main, new_main in main_folders_mapping.items():
        if os.path.exists(old_main):
            print(f"Renaming service folder: {old_main} -> {new_main}")
            os.rename(old_main, new_main)
        else:
            print(f"Service folder not found (already renamed or missing): {old_main}")

def update_file_links():
    print("\n=== Step 3: Updating links in HTML/PHP/XML files ===")
    
    # We will search files in the current directory and all renamed directories
    all_files = []
    
    # Files in the root directory
    for f in os.listdir('.'):
        if os.path.isfile(f) and (f.endswith('.html') or f.endswith('.php') or f.endswith('.xml')):
            all_files.append(os.path.abspath(f))
            
    # Files in all service folders (now Cyrillic)
    for service_dir in main_folders_mapping.values():
        if os.path.exists(service_dir):
            for root, dirs, files in os.walk(service_dir):
                for f in files:
                    if f.endswith('.html') or f.endswith('.php') or f.endswith('.xml'):
                        all_files.append(os.path.abspath(os.path.join(root, f)))
                        
    # Files in other directories just in case (e.g. spasibo)
    for folder in ['spasibo']:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for f in files:
                    if f.endswith('.html') or f.endswith('.php') or f.endswith('.xml'):
                        all_files.append(os.path.abspath(os.path.join(root, f)))

    files_modified = 0
    
    # Build replacements
    # 1. Main folders
    replacements = {}
    for old, new in main_folders_mapping.items():
        replacements[f'/{old}/'] = f'/{new}/'
        replacements[f'"{old}/'] = f'"{new}/'
        replacements[f'\'{old}/'] = f'\'{new}/'
        replacements[f'/{old}"'] = f'/{new}"'
        replacements[f'/{old}\''] = f'/{new}\''
        # Relative paths e.g. ../irkutsk-stiralnie-mashini/
        replacements[f'../{old}/'] = f'../{new}/'
        replacements[f'../../{old}/'] = f'../../{new}/'
        
    # 2. District folders
    for old, new in district_folders_mapping.items():
        replacements[f'/{old}/'] = f'/{new}/'
        replacements[f'"{old}/'] = f'"{new}/'
        replacements[f'\'{old}/'] = f'\'{new}/'
        replacements[f'/{old}"'] = f'/{new}"'
        replacements[f'/{old}\''] = f'/{new}\''
        # Relative paths
        replacements[f'../{old}/'] = f'../{new}/'
        replacements[f'../../{old}/'] = f'../../{new}/'

    for filepath in all_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # Apply replacements
        for target, replacement in replacements.items():
            content = content.replace(target, replacement)
            
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated links in: {os.path.relpath(filepath, '.')}")
            files_modified += 1
            
    print(f"Updated links in {files_modified} files.")

if __name__ == "__main__":
    rename_folders()
    update_file_links()
    print("Reversion to Cyrillic completed.")

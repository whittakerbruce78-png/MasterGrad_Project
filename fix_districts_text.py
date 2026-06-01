import os
import re

districts_map = {
    'centralniy-raion': ('Центральный', 'Центральном'),
    'industrialniy-raion': ('Индустриальный', 'Индустриальном'),
    'kirovskiy-raion': ('Кировский', 'Кировском'),
    'krasnoflotskiy-raion': ('Краснофлотский', 'Краснофлотском'),
    'zheleznodorozhniy-raion': ('Железнодорожный', 'Железнодорожном'),
    'leninskiy-raion': ('Ленинский', 'Ленинском'),
    'oktyabrskiy-raion': ('Октябрьский', 'Октябрьском'),
    'pravoberezhniy-raion': ('Правобережный', 'Правобережном'),
    'sverdlovskiy-raion': ('Свердловский', 'Свердловском'),
    'ленинский-район': ('Ленинский', 'Ленинском'),
    'первомайский-район': ('Первомайский', 'Первомайском'),
    'первореченский-район': ('Первореченский', 'Первореченском'),
    'советский-район': ('Советский', 'Советском'),
    'фрунзенский-район': ('Фрунзенский', 'Фрунзенском'),
}

# All possible source districts that might be in the text incorrectly
wrong_districts = [
    'Ленинский', 'Ленинском', 
    'Первомайский', 'Первомайском', 
    'Первореченский', 'Первореченском', 
    'Советский', 'Советском', 
    'Фрунзенский', 'Фрунзенском',
    'Центральный', 'Центральном',
    'Индустриальный', 'Индустриальном',
    'Кировский', 'Кировском',
    'Краснофлотский', 'Краснофлотском',
    'Железнодорожный', 'Железнодорожном',
    'Октябрьский', 'Октябрьском',
    'Правобережный', 'Правобережном',
    'Свердловский', 'Свердловском'
]

def fix_districts_text():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                norm_path = fpath.replace('\\', '/').lstrip('./')
                parts = norm_path.split('/')
                
                # Check if file is in a district folder
                if len(parts) >= 3 and parts[1] in districts_map:
                    target_nom, target_prep = districts_map[parts[1]]
                elif len(parts) == 3 and parts[1] in districts_map:
                    target_nom, target_prep = districts_map[parts[1]]
                elif len(parts) == 2 and parts[0] != '.' and parts[1] != 'index.html':
                    # some are root/district/index.html
                    dir_name = parts[1]
                    if dir_name == 'index.html':
                        dir_name = parts[0]
                    if dir_name in districts_map:
                        target_nom, target_prep = districts_map[dir_name]
                    else:
                        continue
                else:
                    continue

                # Wait, if we replace blindly, we might replace "Ленинском" with "Кировском" correctly.
                # Let's read and replace
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                original_content = content
                
                # Replace any wrong district name with the target one
                # Need to be careful not to replace it in the menu or chips where we WANT other districts
                # So let's temporarily hide the "other-districts" and "city-dropdown" and "menu"
                
                chips_match = re.search(r'<div class="other-districts".*?</div>', content, flags=re.DOTALL)
                chips = chips_match.group(0) if chips_match else ""
                if chips: content = content.replace(chips, '___CHIPS___')
                
                dropdown_match = re.search(r'<div class="city-dropdown-content">.*?</div>', content, flags=re.DOTALL)
                dropdown = dropdown_match.group(0) if dropdown_match else ""
                if dropdown: content = content.replace(dropdown, '___DROPDOWN___')

                # Replace nominative
                for wrong in ['Ленинский', 'Первомайский', 'Первореченский', 'Советский', 'Фрунзенский', 'Центральный', 'Индустриальный', 'Кировский', 'Краснофлотский', 'Железнодорожный', 'Октябрьский', 'Правобережный', 'Свердловский']:
                    if wrong != target_nom:
                        content = re.sub(rf'\b{wrong}\b', target_nom, content)
                        
                # Replace prepositional
                for wrong in ['Ленинском', 'Первомайском', 'Первореченском', 'Советском', 'Фрунзенском', 'Центральном', 'Индустриальном', 'Кировском', 'Краснофлотском', 'Железнодорожном', 'Октябрьском', 'Правобережном', 'Свердловском']:
                    if wrong != target_prep:
                        content = re.sub(rf'\b{wrong}\b', target_prep, content)

                if chips: content = content.replace('___CHIPS___', chips)
                if dropdown: content = content.replace('___DROPDOWN___', dropdown)
                
                if content != original_content:
                    with open(fpath, 'w', encoding='utf-8') as file:
                        file.write(content)

if __name__ == '__main__':
    fix_districts_text()

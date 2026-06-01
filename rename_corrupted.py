import os
import shutil

khabarovsk_mapping = {
    'ленинский-район': ('industrialniy-raion', 'Индустриальный район', 'Индустриальном'),
    'первореченский-район': ('kirovskiy-raion', 'Кировский район', 'Кировском'),
    'советский-район': ('krasnoflotskiy-raion', 'Краснофлотский район', 'Краснофлотском'),
    'первомайский-район': ('centralniy-raion', 'Центральный район', 'Центральном'),
    'фрунзенский-район': ('zheleznodorozhniy-raion', 'Железнодорожный район', 'Железнодорожном')
}

irkutsk_mapping = {
    'ленинский-район': ('pravoberezhniy-raion', 'Правобережный район', 'Правобережном'),
    'первореченский-район': ('oktyabrskiy-raion', 'Октябрьский район', 'Октябрьском'),
    'советский-район': ('sverdlovskiy-raion', 'Свердловский район', 'Свердловском'),
    'первомайский-район': ('leninskiy-raion', 'Ленинский район', 'Ленинском'),
    'фрунзенский-район': (None, None, None)
}

# Add both normal and corrupted versions to mapping
def get_corrupted_name(s):
    try:
        return s.encode('utf-8').decode('cp1251')
    except:
        return None

for base_dir in os.listdir('.'):
    if not os.path.isdir(base_dir): continue
    
    city = None
    if 'khabarovsk' in base_dir: city = 'khabarovsk'
    elif 'irkutsk' in base_dir: city = 'irkutsk'
    
    if city:
        mapping = khabarovsk_mapping if city == 'khabarovsk' else irkutsk_mapping
        
        for old_dir in mapping.keys():
            corrupted = get_corrupted_name(old_dir)
            names_to_check = [old_dir]
            if corrupted:
                names_to_check.append(corrupted)
                
            for name in set(names_to_check):
                old_path = os.path.join(base_dir, name)
                if os.path.exists(old_path):
                    new_dir = mapping[old_dir][0]
                    if new_dir is None:
                        print("Deleting", old_path)
                        shutil.rmtree(old_path)
                    else:
                        new_path = os.path.join(base_dir, new_dir)
                        if not os.path.exists(new_path):
                            print("Renaming", old_path, "to", new_path)
                            os.rename(old_path, new_path)
                        else:
                            print("Already exists:", new_path)

print("Folders renamed successfully!")

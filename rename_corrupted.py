import os

vladivostok_dirs = [
    'vladivostok-stiralnie-mashini',
    'vladivostok-holodilniki',
    'vladivostok-vodonagrevateli',
    'vladivostok-posudomoechnie-mashini'
]

district_mapping = {
    'Р»РµРЅРёРЅСЃРєРёР№-СЂР°Р№РѕРЅ': 'leninskiy-raion',
    'РїРµСЂРІРѕРјР°Р№СЃРєРёР№-СЂР°Р№РѕРЅ': 'pervomaiskiy-raion',
    'РїРµСЂРІРѕСЂРµС‡РµРЅСЃРєРёР№-СЂР°Р№РѕРЅ': 'pervorechenskiy-raion',
    'СЃРѕРІРµС‚СЃРєРёР№-СЂР°Р№РѕРЅ': 'sovetskiy-raion',
    'С„СЂСѓРЅР·РµРЅСЃРєРёР№-СЂР°Р№РѕРЅ': 'frunzenskiy-raion',
    
    'ленинский-район': 'leninskiy-raion',
    'первомайский-район': 'pervomaiskiy-raion',
    'первореченский-район': 'pervorechenskiy-raion',
    'советский-район': 'sovetskiy-raion',
    'фрунзенский-район': 'frunzenskiy-raion'
}

for v_dir in vladivostok_dirs:
    if not os.path.exists(v_dir):
        print(f"Directory {v_dir} does not exist.")
        continue
    
    print(f"Checking subdirectories in: {v_dir}")
    subdirs = os.listdir(v_dir)
    for sub in subdirs:
        sub_path = os.path.join(v_dir, sub)
        if os.path.isdir(sub_path):
            if sub in district_mapping:
                new_sub = district_mapping[sub]
                new_sub_path = os.path.join(v_dir, new_sub)
                print(f"  Renaming: {sub_path} -> {new_sub_path}")
                os.rename(sub_path, new_sub_path)
            else:
                # Try decoding
                try:
                    decoded = sub.encode('cp1251').decode('utf-8')
                    if decoded in district_mapping:
                        new_sub = district_mapping[decoded]
                        new_sub_path = os.path.join(v_dir, new_sub)
                        print(f"  Renaming (decoded cp1251->utf8): {sub_path} -> {new_sub_path}")
                        os.rename(sub_path, new_sub_path)
                        continue
                except Exception:
                    pass
                try:
                    decoded = sub.encode('utf-8').decode('cp1251')
                    if decoded in district_mapping:
                        new_sub = district_mapping[decoded]
                        new_sub_path = os.path.join(v_dir, new_sub)
                        print(f"  Renaming (decoded utf8->cp1251): {sub_path} -> {new_sub_path}")
                        os.rename(sub_path, new_sub_path)
                        continue
                except Exception:
                    pass

print("District rename complete.")

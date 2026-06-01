import os
import urllib.parse

cities = {
    "khabarovsk": {
        "Name": "Хабаровск",
        "Name_e": "Хабаровске",
        "Name_a": "Хабаровска",
        "prefix": "khabarovsk"
    },
    "irkutsk": {
        "Name": "Иркутск",
        "Name_e": "Иркутске",
        "Name_a": "Иркутска",
        "prefix": "irkutsk"
    }
}

services = {
    "стиральные-машины-владивосток": "stiralnie-mashini",
    "холодильники-владивосток": "holodilniki",
    "водонагреватели-владивосток": "vodonagrevateli",
    "посудомоечные-машины-владивосток": "posudomoechnie-mashini"
}

def process_file(filepath, city_key):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    city = cities[city_key]

    # text replacements
    content = content.replace("Владивостоке", city["Name_e"])
    content = content.replace("Владивостока", city["Name_a"])
    content = content.replace("Владивосток", city["Name"])

    # URL path replacements
    for ru_svc, en_svc in services.items():
        new_path = f"{city['prefix']}-{en_svc}"
        # Replace unencoded
        content = content.replace(ru_svc, new_path)
        # Replace encoded
        encoded_ru_svc = urllib.parse.quote(ru_svc)
        content = content.replace(encoded_ru_svc, new_path)
        
        # also replace lower-case versions of the path name in russian without dashes just in case
        content = content.replace("владивосток", city["Name"].lower())

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for city_key in cities.keys():
    for en_svc in services.values():
        folder = f"{city_key}-{en_svc}"
        filepath = os.path.join(folder, "index.html")
        if os.path.exists(filepath):
            process_file(filepath, city_key)
            print(f"Processed {filepath}")
        else:
            print(f"Missing {filepath}")

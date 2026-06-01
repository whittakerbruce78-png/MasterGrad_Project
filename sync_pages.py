import os

def sync_city_pages():
    with open('index.html', 'r', encoding='utf-8') as f:
        vladivostok_content = f.read()

    cities = [
        {"name": "Хабаровск", "name_prep": "Хабаровске", "folder": "khabarovsk-stiralnie-mashini", "id": "khabarovsk"},
        {"name": "Иркутск", "name_prep": "Иркутске", "folder": "irkutsk-stiralnie-mashini", "id": "irkutsk"}
    ]

    for city in cities:
        content = vladivostok_content
        
        # Replace city names (case-sensitive replacements for Title case and lowercase)
        content = content.replace("Владивосток", city["name"])
        content = content.replace("Владивостоке", city["name_prep"])
        content = content.replace("владивосток", city["id"])
        
        # Fix the dropdown highlight
        # In vladivostok_content, vladivostok has the style="font-weight:bold; color:#0066cc;"
        active_style = 'style="font-weight:bold; color:#0066cc;"'
        
        # Remove active style from Vladivostok
        content = content.replace(
            f'<a href="/" {active_style}>г. Владивосток</a>',
            '<a href="/" >г. Владивосток</a>'
        )
        
        # Add active style to current city
        content = content.replace(
            f'<a href="/{city["folder"]}/" >г. {city["name"]}</a>',
            f'<a href="/{city["folder"]}/" {active_style}>г. {city["name"]}</a>'
        )

        # Save to the city's index.html
        filepath = os.path.join(city["folder"], 'index.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

sync_city_pages()
print("City index pages synchronized with Vladivostok!")

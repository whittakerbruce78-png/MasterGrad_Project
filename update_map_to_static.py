import os
import re

khabarovsk_replacement = """<div class="map-section">
        <h3 style="font-size: 24px; color: #222; font-weight: 700; margin-bottom: 10px; text-align: center;">
          Наш офис г.Владивосток ул.Жигура 26а
        </h3>
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06);">
          <a href="https://yandex.ru/maps/114/khabarovsk/?ll=135.068305%2C48.474136&z=15" target="_blank" style="display:block;">
            <img src="https://static-maps.yandex.ru/1.x/?ll=135.068305,48.474136&size=500,320&z=15&l=map&pt=135.068305,48.474136,pm2blm" alt="Мастер-град.рф на карте Хабаровска" style="display: block; width: 100%; height: auto; object-fit: cover;">
          </a>
        </div>
      </div>"""

irkutsk_replacement = """<div class="map-section">
        <h3 style="font-size: 24px; color: #222; font-weight: 700; margin-bottom: 10px; text-align: center;">
          Наш офис г.Владивосток ул.Жигура 26а
        </h3>
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06);">
          <a href="https://yandex.ru/maps/63/irkutsk/?ll=104.281822%2C52.281226&z=15" target="_blank" style="display:block;">
            <img src="https://static-maps.yandex.ru/1.x/?ll=104.281822,52.281226&size=500,320&z=15&l=map&pt=104.281822,52.281226,pm2blm" alt="Мастер-град.рф на карте Иркутска" style="display: block; width: 100%; height: auto; object-fit: cover;">
          </a>
        </div>
      </div>"""

pattern = re.compile(r'<div class="map-section">.*?</div>\s*</div>', re.DOTALL)

for root, dirs, files in os.walk('.'):
    city = None
    if 'khabarovsk' in root: city = 'khabarovsk'
    elif 'irkutsk' in root: city = 'irkutsk'
    
    if city:
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_section = khabarovsk_replacement if city == 'khabarovsk' else irkutsk_replacement
                    
                    if pattern.search(content):
                        content = pattern.sub(new_section, content)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

print("Map reverted to static with pin and original text!")

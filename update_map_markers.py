import os
import re

khabarovsk_replacement = """<div class="map-section">
        <h3 style="font-size: 24px; color: #222; font-weight: 700; margin-bottom: 5px; text-align: center;">
          Работаем по всему Хабаровску, а также по всем районам
        </h3>
        <p style="text-align: center; color: #666; margin-bottom: 15px; font-size: 16px;">
          Адрес: г. Хабаровск, ул. Муравьева-Амурского, 4 (только выезд мастера)
        </p>
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06);">
          <iframe src="https://yandex.ru/map-widget/v1/?mode=search&text=Хабаровск,%20ул.%20Муравьева-Амурского,%204&z=15" width="100%" height="320" frameborder="0" allowfullscreen="true" style="display:block;"></iframe>
        </div>
      </div>"""

irkutsk_replacement = """<div class="map-section">
        <h3 style="font-size: 24px; color: #222; font-weight: 700; margin-bottom: 5px; text-align: center;">
          Работаем по всему Иркутску, а также по всем районам
        </h3>
        <p style="text-align: center; color: #666; margin-bottom: 15px; font-size: 16px;">
          Адрес: г. Иркутск, ул. Ленина, 14 (только выезд мастера)
        </p>
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06);">
          <iframe src="https://yandex.ru/map-widget/v1/?mode=search&text=Иркутск,%20ул.%20Ленина,%2014&z=15" width="100%" height="320" frameborder="0" allowfullscreen="true" style="display:block;"></iframe>
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

print("Map headers and iframes updated successfully!")

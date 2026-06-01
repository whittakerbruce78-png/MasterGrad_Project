import os
import re

khabarovsk_map = """<!-- БЛОК Карта (Хабаровск) -->
<section class="district-info" style="padding: 30px 20px; margin: 30px 0; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 12px;">
  <div class="district-container">
    <div class="district-grid">

      <!-- Карта (на мобильных идёт первой) -->
      <div class="map-section">
        <h3 style="font-size: 24px; color: #222; font-weight: 700; margin-bottom: 10px; text-align: center;">
          Зона обслуживания: Хабаровск и пригород
        </h3>
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06);">
          <iframe src="https://yandex.ru/map-widget/v1/?ll=135.071917%2C48.482717&z=11" width="100%" height="320" frameborder="0" allowfullscreen="true" style="display:block;"></iframe>
        </div>
      </div>

      <!-- Призыв к действию (на мобильных идут после карты) -->
      <div class="buttons-section" style="display:flex; flex-direction:column; justify-content:center; align-items:center;">
        <h2 class="district-title" style="margin-bottom:15px; text-align:center;">Нужен мастер прямо сейчас?</h2>
        <p style="font-size: 16px; color: #555; text-align: center; margin-bottom: 25px; line-height:1.5;">
          Наш специалист уже находится в вашем районе. Оставьте заявку, и мы приедем в течение 20-40 минут. Без выходных!
        </p>
        <a href="tel:+79143331700" style="display:inline-block; padding:15px 30px; background:#0066cc; color:#fff; text-decoration:none; font-weight:bold; font-size:18px; border-radius:30px; box-shadow:0 4px 15px rgba(0,102,204,0.3); transition:all 0.3s;">
          +7 (914) 333-17-00
        </a>
      </div>
    </div>
  </div>
</section>"""

irkutsk_map = """<!-- БЛОК Карта (Иркутск) -->
<section class="district-info" style="padding: 30px 20px; margin: 30px 0; background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); border-radius: 12px;">
  <div class="district-container">
    <div class="district-grid">

      <!-- Карта (на мобильных идёт первой) -->
      <div class="map-section">
        <h3 style="font-size: 24px; color: #222; font-weight: 700; margin-bottom: 10px; text-align: center;">
          Зона обслуживания: Иркутск и пригород
        </h3>
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06);">
          <iframe src="https://yandex.ru/map-widget/v1/?ll=104.280606%2C52.289588&z=11" width="100%" height="320" frameborder="0" allowfullscreen="true" style="display:block;"></iframe>
        </div>
      </div>

      <!-- Призыв к действию (на мобильных идут после карты) -->
      <div class="buttons-section" style="display:flex; flex-direction:column; justify-content:center; align-items:center;">
        <h2 class="district-title" style="margin-bottom:15px; text-align:center;">Нужен мастер прямо сейчас?</h2>
        <p style="font-size: 16px; color: #555; text-align: center; margin-bottom: 25px; line-height:1.5;">
          Наш специалист уже находится в вашем районе. Оставьте заявку, и мы приедем в течение 20-40 минут. Без выходных!
        </p>
        <a href="tel:+79143331700" style="display:inline-block; padding:15px 30px; background:#0066cc; color:#fff; text-decoration:none; font-weight:bold; font-size:18px; border-radius:30px; box-shadow:0 4px 15px rgba(0,102,204,0.3); transition:all 0.3s;">
          +7 (914) 333-17-00
        </a>
      </div>
    </div>
  </div>
</section>"""


pattern = re.compile(r'<!-- БЛОК "Мы на Яндекс.Картах" — адаптирован под мобильные -->.*?</section>', re.DOTALL | re.IGNORECASE)
pattern2 = re.compile(r'<!-- БЛОК Карта \(.*?\) -->.*?</section>', re.DOTALL | re.IGNORECASE)

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
                    
                    new_map = khabarovsk_map if city == 'khabarovsk' else irkutsk_map
                    
                    if pattern.search(content):
                        content = pattern.sub(new_map, content)
                    elif pattern2.search(content):
                        content = pattern2.sub(new_map, content)
                        
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

print("Maps updated successfully!")

import os
import re

original_buttons = """<!-- Кнопки (на мобильных идут после карты) -->
      <div class="buttons-section">
        <h2 class="district-title">Мы на Картах</h2>

        <!-- Кнопка 2GIS (сверху на десктопе и мобильных) -->
        <a href="https://2gis.ru/vladivostok/firm/70000001104628462/tab/reviews?m=131.927441%2C43.129851%2F17.91&utm_source=widget_firm"
           target="_blank"
           class="review-btn review-btn--2gis">
          <img src="../img/partner2.png" alt="2GIS" class="review-logo">
          <span class="review-text">оставить отзыв</span>
        </a>

        <!-- Кнопка Яндекс.Карты (снизу) -->
        <a href="https://yandex.com.tr/maps/org/master_grad_rf/242047769764/reviews/?ll=131.927140%2C43.129808&utm_content=more-reviews&utm_medium=reviews&utm_source=maps-reviews-widget&z=17"
           target="_blank"
           class="review-btn review-btn--yandex">
          <img src="../img/yandexkarty.png" alt="Яндекс.Карты" class="review-logo">
          <span class="review-text">оставить отзыв</span>
        </a>
      </div>"""

pattern = re.compile(r'<!-- Призыв к действию \(на мобильных идут после карты\) -->.*?</div>\s*</div>\s*</div>\s*</section>', re.DOTALL)

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
                    
                    if pattern.search(content):
                        # Replace the custom CTA back with the original buttons + closing tags
                        replacement = original_buttons + "\n    </div>\n  </div>\n</section>"
                        content = pattern.sub(replacement, content)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

print("Buttons reverted successfully!")

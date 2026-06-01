import os
import re

def clean_and_inject(filepath, is_main=False, current_city="vladivostok"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove old header-city-switcher
    # The switcher block has <div class="header-city-switcher" ...> ... </div>
    # Let's find it with regex or string search
    start_str = '<div class="header-city-switcher"'
    end_str = '</div>\n        <a href="tel:+79143331700"'
    
    if start_str in content and end_str in content:
        s_idx = content.find(start_str)
        e_idx = content.find('</div>', s_idx) + 6
        # Remove it
        content = content[:s_idx].rstrip() + '\n        <a href="tel:+79143331700"' + content[content.find('class="phone-number"', s_idx)-27:]

    # A more robust regex removal for header-city-switcher
    content = re.sub(r'<div class="header-city-switcher".*?</select>\s*</div>', '', content, flags=re.DOTALL)
    
    # 2. Remove city-choice-block
    content = re.sub(r'<!-- Блок выбора города -->.*?</section>', '', content, flags=re.DOTALL)
    
    # 3. Replace menu-bar
    old_menu_bar = '<button class="menu-bar" id="menu-btn" aria-label="Открыть меню" aria-expanded="false" aria-controls="sidebar">Меню</button>'
    
    new_menu_bar = f"""<div class="menu-bar" style="gap: 20px;">
      <button id="menu-btn" aria-label="Открыть меню" aria-expanded="false" aria-controls="sidebar" style="background: none; border: none; color: white; font-size: 18px; font-weight: bold; cursor: pointer; padding: 0; outline: none;">Меню</button>
      <select onchange="location = this.value;" style="padding: 2px 10px; border-radius: 4px; border: none; font-family: 'Onest', sans-serif; font-size: 14px; background-color: white; color: #333; cursor: pointer; outline: none; font-weight: normal; max-height: 24px;">
          <option value="/"{' selected' if current_city == 'vladivostok' else ''}>г. Владивосток</option>
          <option value="/khabarovsk-stiralnie-mashini/"{' selected' if current_city == 'khabarovsk' else ''}>г. Хабаровск</option>
          <option value="/irkutsk-stiralnie-mashini/"{' selected' if current_city == 'irkutsk' else ''}>г. Иркутск</option>
      </select>
    </div>"""

    # Wait, what if it's already a div?
    if '<div class="menu-bar"' in content:
        # Re-replace just in case we are running it twice
        content = re.sub(r'<div class="menu-bar" style="gap: 20px;">.*?</div>', new_menu_bar, content, flags=re.DOTALL)
    else:
        content = content.replace(old_menu_bar, new_menu_bar)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Process all files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            city = "vladivostok"
            if "khabarovsk" in root:
                city = "khabarovsk"
            elif "irkutsk" in root:
                city = "irkutsk"
            clean_and_inject(filepath, is_main=(file == 'index.html' and root == '.'), current_city=city)
print("UI adjustments applied.")

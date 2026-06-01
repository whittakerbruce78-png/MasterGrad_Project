import os

def inject_header(filepath, is_main=False, current_city="vladivostok"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Header injection
    if '<div class="header-container">' in content and 'header-city-switcher' not in content:
        switcher_html = f"""
        <div class="header-city-switcher" style="margin-left: auto; margin-right: 15px; display: flex; align-items: center;">
            <select onchange="location = this.value;" style="padding: 6px 12px; border-radius: 6px; border: 1px solid #ccc; font-family: 'Onest', sans-serif; font-size: 14px; background-color: #fff; cursor: pointer; outline: none;">
                <option value="/"{' selected' if current_city == 'vladivostok' else ''}>г. Владивосток</option>
                <option value="/khabarovsk-stiralnie-mashini/"{' selected' if current_city == 'khabarovsk' else ''}>г. Хабаровск</option>
                <option value="/irkutsk-stiralnie-mashini/"{' selected' if current_city == 'irkutsk' else ''}>г. Иркутск</option>
            </select>
        </div>
"""
        # We find phone number anchor
        target_phone = '<a href="tel:+79143331700" class="phone-number"'
        if target_phone in content:
            content = content.replace(target_phone, switcher_html + '        ' + target_phone)

    # 2. Main Page Block Injection (only for index.html)
    if is_main and 'city-choice-block' not in content:
        # Insert after <section class="services" ... </section>
        target_services_end = "</ul>\n      </section>"
        if target_services_end in content:
            city_block = """

      <!-- Блок выбора города -->
      <section class="city-choice-block" style="text-align: center; margin: 30px 15px; padding: 25px 15px; background: #f4f7f6; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h2 style="font-size: 22px; margin-bottom: 20px; font-weight: 600; color: #333;">Выберите ваш город:</h2>
        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
          <a href="/" style="display: inline-block; padding: 10px 20px; background: #0066cc; color: white; text-decoration: none; border-radius: 30px; font-weight: 500; font-size: 15px; transition: 0.3s; box-shadow: 0 4px 10px rgba(0,102,204,0.3);">Владивосток</a>
          <a href="/khabarovsk-stiralnie-mashini/" style="display: inline-block; padding: 10px 20px; background: #fff; color: #0066cc; text-decoration: none; border: 1px solid #0066cc; border-radius: 30px; font-weight: 500; font-size: 15px; transition: 0.3s;">Хабаровск</a>
          <a href="/irkutsk-stiralnie-mashini/" style="display: inline-block; padding: 10px 20px; background: #fff; color: #0066cc; text-decoration: none; border: 1px solid #0066cc; border-radius: 30px; font-weight: 500; font-size: 15px; transition: 0.3s;">Иркутск</a>
        </div>
      </section>"""
            content = content.replace(target_services_end, target_services_end + city_block)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Process main file
if os.path.exists('index.html'):
    inject_header('index.html', is_main=True, current_city="vladivostok")
    print("Injected into main index.html")

# Process other files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file == 'index.html' and root != '.':
            filepath = os.path.join(root, file)
            city = "vladivostok"
            if "khabarovsk" in root:
                city = "khabarovsk"
            elif "irkutsk" in root:
                city = "irkutsk"
            inject_header(filepath, is_main=False, current_city=city)
            print(f"Injected into {filepath}")

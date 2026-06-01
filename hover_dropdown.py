import os
import re

def clean_and_inject(filepath, current_city="vladivostok"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Identify the current menu-bar div that we injected last time
    # It starts with <div class="menu-bar" style="gap: 20px;">
    # and ends with </div> right after the </select>
    
    new_menu_bar = f"""<style>
.city-dropdown-container {{
    position: relative;
    display: inline-block;
}}
.city-dropbtn {{
    background-color: #61A8C5; /* Немного темнее основного #73BAD7 */
    color: white;
    padding: 3px 15px;
    font-size: 16px;
    border: 2px solid #eaf3f8; /* Цвет светлого фона */
    border-radius: 25px;
    cursor: pointer;
    font-family: 'Onest', sans-serif;
    font-weight: 500;
    transition: 0.3s;
}}
.city-dropbtn:hover {{
    background-color: #5097b4;
}}
.city-dropdown-content {{
    display: none;
    position: absolute;
    background-color: #ffffff;
    min-width: 170px;
    box-shadow: 0px 10px 20px rgba(0,0,0,0.15);
    z-index: 1001;
    border-radius: 12px;
    overflow: hidden;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 5px;
}}
.city-dropdown-container:hover .city-dropdown-content {{
    display: block;
}}
.city-dropdown-content a {{
    color: #333;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    font-family: 'Onest', sans-serif;
    font-size: 15px;
    text-align: center;
    border-bottom: 1px solid #f0f0f0;
    transition: 0.2s;
}}
.city-dropdown-content a:last-child {{
    border-bottom: none;
}}
.city-dropdown-content a:hover {{
    background-color: #f8f9fa;
    color: #0066cc;
    font-weight: bold;
}}
</style>

<div class="menu-bar" style="gap: 40px;">
    <button id="menu-btn" aria-label="Открыть меню" aria-expanded="false" aria-controls="sidebar" style="background: none; border: none; color: white; font-size: 18px; font-weight: bold; cursor: pointer; padding: 0; outline: none;">Меню</button>
    
    <div class="city-dropdown-container">
        <button class="city-dropbtn">Выбрать город ▼</button>
        <div class="city-dropdown-content">
            <a href="/" {'style="font-weight:bold; color:#0066cc;"' if current_city == 'vladivostok' else ''}>г. Владивосток</a>
            <a href="/khabarovsk-stiralnie-mashini/" {'style="font-weight:bold; color:#0066cc;"' if current_city == 'khabarovsk' else ''}>г. Хабаровск</a>
            <a href="/irkutsk-stiralnie-mashini/" {'style="font-weight:bold; color:#0066cc;"' if current_city == 'irkutsk' else ''}>г. Иркутск</a>
        </div>
    </div>
</div>"""

    # We need to replace the old <div class="menu-bar"...</div> block
    # Note: we might have multiple <style> blocks if we run this multiple times, so let's clean up old ones
    content = re.sub(r'<style>\s*\.city-dropdown-container.*?</style>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="menu-bar" style="gap: 20px;">.*?</div>', new_menu_bar, content, flags=re.DOTALL)
    content = re.sub(r'<div class="menu-bar" style="gap: 40px;">.*?</div>', new_menu_bar, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            city = "vladivostok"
            if "khabarovsk" in root:
                city = "khabarovsk"
            elif "irkutsk" in root:
                city = "irkutsk"
            clean_and_inject(filepath, current_city=city)
print("Hover dropdown applied.")

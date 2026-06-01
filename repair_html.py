import os
import re

def repair_html(filepath, current_city="vladivostok"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the corrupted phone number tag
    content = content.replace('<a href="tel:+79143331700"<a href="tel:+79143331700"', '<a href="tel:+79143331700"')

    # 2. Extract the safe parts of the document
    # We want to replace everything from the closing </div> of header-container
    # to the opening <nav id="sidebar"
    
    # Find <div class="header-container">
    header_start = content.find('<div class="header-container">')
    if header_start == -1:
        return
        
    # The header-container ends with </a> \n      </div>
    # Let's use regex to find the block to replace:
    # From: </a>\s*</div>  (right after the phone number)
    # To: <nav id="sidebar"
    
    pattern = r'(<a href="tel:\+79143331700".*?</a>\s*</div>).*?(<nav id="sidebar")'
    
    new_menu_bar = f"""
<style>
.city-dropdown-container {{
    position: relative;
    display: inline-block;
    padding-bottom: 20px;
    margin-bottom: -20px;
}}
.city-dropbtn {{
    background-color: #73BAD7;
    color: white;
    padding: 2px 15px;
    font-size: 16px;
    border: 1px solid #82c8e6;
    border-radius: 15px;
    cursor: pointer;
    font-family: 'Onest', sans-serif;
    font-weight: bold;
    transition: 0.3s;
    outline: none;
}}
.city-dropbtn:hover {{
    background-color: #63a9c7;
}}
.city-dropdown-content {{
    display: none;
    position: absolute;
    background-color: #ffffff;
    min-width: 170px;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
    z-index: 1001;
    border-radius: 8px;
    overflow: hidden;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: -2px;
}}
.city-dropdown-container:hover .city-dropdown-content {{
    display: block;
}}
.city-dropdown-content a {{
    color: #333;
    padding: 10px 16px;
    text-decoration: none;
    display: block;
    font-family: 'Onest', sans-serif;
    font-size: 15px;
    text-align: center;
    border-bottom: 1px solid #e0e0e0;
    transition: 0.2s;
}}
.city-dropdown-content a:last-child {{
    border-bottom: none;
}}
.city-dropdown-content a:hover {{
    background-color: #f1f1f1;
    color: #0066cc;
}}
</style>

      <div class="menu-bar" style="gap: 30px;">
          <button id="menu-btn" aria-label="Открыть меню" aria-expanded="false" aria-controls="sidebar" style="background: none; border: none; color: white; font-size: 18px; font-weight: bold; cursor: pointer; padding: 0; outline: none; margin: 0;">Меню</button>
          
          <div class="city-dropdown-container">
              <button class="city-dropbtn">Выбрать город ▼</button>
              <div class="city-dropdown-content">
                  <a href="/" {'style="font-weight:bold; color:#0066cc;"' if current_city == 'vladivostok' else ''}>г. Владивосток</a>
                  <a href="/khabarovsk-stiralnie-mashini/" {'style="font-weight:bold; color:#0066cc;"' if current_city == 'khabarovsk' else ''}>г. Хабаровск</a>
                  <a href="/irkutsk-stiralnie-mashini/" {'style="font-weight:bold; color:#0066cc;"' if current_city == 'irkutsk' else ''}>г. Иркутск</a>
              </div>
          </div>
      </div>
      """

    # Clean up previous <style> blocks that might be outside this region if any
    content = re.sub(r'<style>\s*\.city-dropdown-container.*?</style>\s*', '', content, flags=re.DOTALL)
    
    # Perform the replacement to restore clean structure
    content = re.sub(pattern, r'\1' + new_menu_bar + r'\2', content, flags=re.DOTALL)

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
            repair_html(filepath, current_city=city)

print("HTML structure repaired successfully!")

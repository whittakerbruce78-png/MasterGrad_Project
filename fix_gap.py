import os

target_style = 'style="font-size: 24px; color: #222; font-weight: 700; margin-top: 0; margin-bottom: 20px; text-align: center;"'
new_style = 'style="font-size: 24px; color: #222; font-weight: 700; margin-top: 0; margin-bottom: 0px; text-align: center;"'

target_map = 'class="map-section" style="display: flex; flex-direction: column; height: 100%;"'
new_map = 'class="map-section" style="display: flex; flex-direction: column; height: 100%; gap: 20px;"'

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changed = False
                
                if target_style in content:
                    content = content.replace(target_style, new_style)
                    changed = True
                    
                if target_map in content:
                    content = content.replace(target_map, new_map)
                    changed = True
                
                if changed:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                print(f"Error in {filepath}: {e}")

print("Gap alignment fixed!")

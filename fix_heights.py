import os
import re

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changed = False
                
                # 1. Change align-items back to stretch in district-grid
                if 'align-items: start;' in content:
                    content = content.replace('align-items: start;', 'align-items: stretch;')
                    changed = True
                    
                # 2. Add flex to map-section
                if '<div class="map-section">' in content:
                    content = content.replace('<div class="map-section">', '<div class="map-section" style="display: flex; flex-direction: column; height: 100%;">')
                    changed = True
                
                # 3. Add flex-grow and relative to the inner div
                old_div = '<div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06);">'
                new_div = '<div style="border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.06); flex-grow: 1; position: relative; min-height: 250px;">'
                if old_div in content:
                    content = content.replace(old_div, new_div)
                    changed = True

                # 4. Fix a tags and img tags inside map-section
                # We can just find the map-section block and replace the styles inside it.
                def repl_map(m):
                    block = m.group(0)
                    # Add style="display:block; width:100%; height:100%;" to <a> if not present or replace existing
                    if 'style="display:block;"' in block:
                        block = block.replace('style="display:block;"', 'style="display:block; width:100%; height:100%;"')
                    else:
                        block = re.sub(r'(<a href="[^"]+" target="_blank")>', r'\1 style="display:block; width:100%; height:100%;">', block)
                    
                    # Replace img styles
                    block = re.sub(r'(<img src="[^"]+"[^>]*alt="[^"]+")\s*style="[^"]+"', r'\1 style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; border: 0;"', block)
                    # If it spans multiple lines
                    block = re.sub(r'(<img src="[^"]+"\s+alt="[^"]+")\s*style="[^"]+"', r'\1 style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; border: 0;"', block, flags=re.DOTALL)
                    
                    return block

                new_content = re.sub(r'<div class="map-section".*?</div>\s*</div>', repl_map, content, flags=re.DOTALL)
                if new_content != content:
                    content = new_content
                    changed = True
                    
                if changed:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                print(f"Error in {filepath}: {e}")

print("Alignment fixed to match heights perfectly!")

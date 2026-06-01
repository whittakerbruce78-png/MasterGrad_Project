import os

errors = []
warnings = []

cities = ["khabarovsk", "irkutsk"]

# 1. Check index.html
try:
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        if "city-choice-block" not in content:
            errors.append("index.html: Отсутствует блок city-choice-block.")
        if "header-city-switcher" not in content:
            errors.append("index.html: Отсутствует переключатель городов в шапке.")
except Exception as e:
    errors.append(f"Ошибка чтения index.html: {e}")

# 2. Check regional files
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            is_regional = False
            city_name = ""
            for c in cities:
                if c in root:
                    is_regional = True
                    city_name = c
                    break
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Check header switcher in ALL files
                if "header-city-switcher" not in content:
                    errors.append(f"{filepath}: Отсутствует переключатель городов.")
                
                # Check regional specifics
                if is_regional:
                    if "Владивосток" in content:
                        warnings.append(f"{filepath}: Найдено слово 'Владивосток' в тексте.")
                    
                    if city_name == "khabarovsk" and "irkutsk-stiralnie-mashini" in content and "khabarovsk-stiralnie-mashini" not in content:
                        # Well, the header switcher actually contains all cities, so it will have irkutsk.
                        pass
                    
                    # Ensure the canonical link is correct
                    if "canonical" in content and "xn----7sbblgc1c8acfl.xn--p1ai" not in content and city_name not in content:
                        warnings.append(f"{filepath}: Canonical link might be incorrect.")

print("Ошибки:", errors if errors else "Нет ошибок")
print("Предупреждения:", warnings if warnings else "Нет предупреждений")

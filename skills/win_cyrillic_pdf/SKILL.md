---
name: win-cyrillic-pdf-generation
description: >-
  Генерация красивых и качественных PDF-отчетов на русском языке с использованием библиотеки fpdf2 на ОС Windows.
  Включает правильный импорт системных шрифтов ttf и устранение ошибок кодировки.
---

# Генерация кириллических PDF на Windows через Python

## Обзор
Стандартные PDF-библиотеки (включая `fpdf2` и `reportlab`) по умолчанию не поддерживают кириллицу при использовании базовых шрифтов (Helvetica, Times). Это приводит к ошибкам компиляции или некорректному отображению текста.

Этот скилл содержит стандартизированный способ генерации русскоязычных PDF-отчетов путем подключения встроенных системных шрифтов ОС Windows.

## Зависимости
- Python 3.x
- Библиотека `fpdf2` (`pip install fpdf2`)

## Шаблон генератора отчетов (scripts/generate_report.py)
Используйте этот шаблон для создания красивого двухколоночного или стандартного структурированного отчета.

```python
import os
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        # Красивая шапка темно-синего цвета
        self.set_fill_color(24, 43, 73)  # Dark Blue
        self.rect(0, 0, 210, 32, 'F')
        
        self.set_text_color(255, 255, 255)
        self.set_y(6)
        self.set_font("ArialBD", "", 16)
        self.cell(0, 8, "ТЕХНИЧЕСКИЙ ОТЧЕТ", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_y(35) # Отступ после шапки

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Страница {self.page_no()}/{{nb}}", align="C")

def generate():
    pdf = PDFReport(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    
    # ПРАВИЛЬНЫЙ ИМПОРТ ШРИФТОВ НА WINDOWS
    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
    pdf.add_font("ArialBD", "", r"C:\Windows\Fonts\arialbd.ttf")
    pdf.add_font("ArialI", "", r"C:\Windows\Fonts\ariali.ttf")
    
    pdf.add_page()
    pdf.set_margins(15, 35, 15)
    
    # Текст отчета
    pdf.set_text_color(33, 37, 41)
    pdf.set_font("ArialBD", "", 12)
    pdf.cell(0, 6, "1. Сводка выполненных работ", new_x="LMARGIN", new_y="NEXT")
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(2)
    
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 5, "Текст отчета на русском языке. Все кодировки отображаются корректно.")
    
    pdf.output("Report.pdf")

if __name__ == "__main__":
    generate()
```

## Важные правила разметки PDF
1. **Кодировка и Спецсимволы**:
   Шрифт Arial поддерживает стандартную кириллицу. Однако, символы вроде буллетов (`•`, `chr(149)`) или специфических стрелок могут вызывать ошибку `missing glyphs`. В качестве буллетов всегда используйте обычный дефис `"-"`.
2. **Перенос строк**:
   Никогда не используйте метод `cell()` для длинного текста. Для абзацев и предложений всегда используйте `multi_cell(0, height, text)`, чтобы включить автоматический перенос строк по ширине страницы.
3. **Верхний и нижний колонтитулы**:
   Используйте `self.alias_nb_pages()` для вывода общего количества страниц во встроенных методах `header()` и `footer()`.

## Решение частых проблем
* **Ошибка `FileNotFoundError` для шрифта**: Убедитесь, что путь `C:\Windows\Fonts\arial.ttf` написан без опечаток и диск C существует. Для кроссплатформенности можно скопировать шрифты в локальную папку проекта `fonts/` и подгружать их оттуда.
* **Выход текста за границы страницы**: Используйте метод `self.set_auto_page_break(auto=True, margin=20)` при инициализации, чтобы страницы нарезались автоматически.

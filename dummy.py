import os
import shutil

for d in os.listdir('.'):
    if not os.path.isdir(d):
        continue
    # we know the dir ends with vladivostok in russian, which has 'vladivostok' in cp1251 or something?
    # actually, let's just use the index of the dir.
    try:
        if "стиральные" in d or d.startswith(bytes([209, 129, 209, 130, 208, 184]).decode('utf-8')):
            pass # this might fail if encoding is wrong
    except:
        pass

# Let's just use a simple regex on all html files in the root to find the right one if we wanted, but it's a dir.
# Let's just do it directly in powershell with Copy-Item

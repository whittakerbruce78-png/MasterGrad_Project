import os
import zipfile

folders_to_include = [
    'css', 'img', 
    'irkutsk-holodilniki', 'irkutsk-posudomoechnie-mashini', 'irkutsk-stiralnie-mashini', 'irkutsk-vodonagrevateli', 
    'khabarovsk-holodilniki', 'khabarovsk-posudomoechnie-mashini', 'khabarovsk-stiralnie-mashini', 'khabarovsk-vodonagrevateli', 
    'script', 'spasibo', 
    'vladivostok-holodilniki', 'vladivostok-posudomoechnie-mashini', 'vladivostok-stiralnie-mashini', 'vladivostok-vodonagrevateli'
]

files_to_include = [
    'index.html', 'index.php', 'preindex.html', 'reviews.html', 
    '.htaccess', 'favicon.ico', 'robots.txt', 'sitemap.xml', 'yandex_fc497593ac46f340.html'
]

archive_name = 'MasterGrad_Project_Deploy.zip'

print("Creating deployment archive...")

with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    # Add folders and their contents
    for folder in folders_to_include:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, '.')
                    zip_file.write(filepath, arcname)
                    print(f"Added: {arcname}")
                    
    # Add files
    for file in files_to_include:
        if os.path.exists(file):
            zip_file.write(file, file)
            print(f"Added: {file}")

print(f"\nSuccess! Created archive: {archive_name}")

import os
import datetime
import urllib.parse

base_url = "https://мастер-град.рф"

new_urls = []
date_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

cities = ["khabarovsk", "irkutsk"]
services = ["stiralnie-mashini", "holodilniki", "vodonagrevateli", "posudomoechnie-mashini"]
districts = ["ленинский-район", "первореченский-район", "советский-район", "первомайский-район", "фрунзенский-район"]

for c in cities:
    for s in services:
        folder = f"{c}-{s}"
        url = f"{base_url}/{folder}/"
        new_urls.append(f"""<url>
  <loc>{url}</loc>
  <lastmod>{date_str}</lastmod>
  <priority>0.80</priority>
</url>""")
        
        for d in districts:
            encoded_d = urllib.parse.quote(d).lower()
            url_dist = f"{base_url}/{folder}/{encoded_d}/"
            new_urls.append(f"""<url>
  <loc>{url_dist}</loc>
  <lastmod>{date_str}</lastmod>
  <priority>0.64</priority>
</url>""")

with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

# insert before </urlset>
insert_pos = sitemap.rfind('</urlset>')
if insert_pos != -1:
    new_sitemap = sitemap[:insert_pos] + '\n'.join(new_urls) + '\n\n' + sitemap[insert_pos:]
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(new_sitemap)
    print("Sitemap updated.")

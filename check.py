import os
import json

transcript_path = r"C:\Users\slavn\.gemini\antigravity\brain\17b7af82-8769-46a8-aa53-05dbf6c006c6\.system_generated\logs\transcript.jsonl"
output_path = r"C:\Users\slavn\Desktop\MasterGrad_Project\credentials_found.txt"

search_terms = ['ftp', 'filezilla', 'beget', 'пароль', 'логин', 'host', 'username', 'password', 'хостинг', 'login']

print("Searching transcript...")
matches = []

if os.path.exists(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_no, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                content = data.get('content', '')
            except Exception:
                content = line
            
            content_lower = content.lower()
            if any(term in content_lower for term in search_terms):
                matches.append(f"Line {line_no}:\n{content}\n" + "-"*50 + "\n")

    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write('\n'.join(matches))
    print(f"Done! Results written to {output_path}")
else:
    print(f"Transcript path does not exist")

import argparse
import os
import zipfile
from pathlib import Path
import requests
import markdown
import sys

TIINY_API_URL = "https://ext.tiiny.host/v1/upload"

def convert_md_to_html(md_text: str, title: str) -> str:
    html_body = markdown.markdown(md_text, extensions=['extra', 'attr_list', 'tables'])
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css">
</head>
<body>
<main class="container">
{html_body}
</main>
</body>
</html>
"""

def convert_file(input_path: Path, output_path: Path):
    with input_path.open("r", encoding="utf-8") as f:
        md_text = f.read()
    html = convert_md_to_html(md_text, input_path.stem)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(html)
    print(f"[✔] Convertito: {input_path.name} → {output_path.name}")

def convert_folder(input_folder: Path, output_zip: Path):
    html_files = []
    for md_file in input_folder.glob("*.md"):
        with md_file.open("r", encoding="utf-8") as f:
            md_text = f.read()
        html = convert_md_to_html(md_text, md_file.stem)
        html_filename = md_file.with_suffix(".html").name
        html_files.append((html_filename, html))

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filename, html_content in html_files:
            zipf.writestr(filename, html_content)
            print(f"[+] Aggiunto allo zip: {filename}")
    print(f"[✔] Archivio completato: {output_zip}")

def upload_to_tiiny(file_path: Path, domain: str = None):
    api_key = os.getenv("TIINY_API_KEY")
    if not api_key:
        print("[❌] Variabile d’ambiente TIINY_API_KEY mancante.")
        sys.exit(1)

    headers = { "x-api-key": api_key }
    files = { "files": (file_path.name, open(file_path, "rb")) }
    data = {}
    if domain:
        data["domain"] = domain

    response = requests.post(TIINY_API_URL, headers=headers, files=files, data=data)
    if response.status_code == 200:
        link = response.json().get("data", {}).get("link")
        print(f"[🌐] Pubblicato: https://{link}")
    else:
        print(f"[❌] Upload fallito: {response.status_code} - {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="File .md o cartella di file .md")
    parser.add_argument("--output", help="Nome del file HTML o ZIP di output")
    parser.add_argument("--domain-prefix", help="Prefisso dominio da usare se --domain non è passato", default="")
    args = parser.parse_args()

    input_path = Path(args.input)
    domain = None

    if input_path.is_file() and input_path.suffix == ".md":
        output_file = Path(args.output) if args.output else input_path.with_suffix(".html")
        convert_file(input_path, output_file)
        domain = f"{args.domain_prefix}-{input_path.stem}".lower() if args.domain_prefix else None
        upload_to_tiiny(output_file, domain=domain)
    elif input_path.is_dir():
        output_zip = Path(args.output) if args.output else input_path.with_name(f"{input_path.name}.zip")
        convert_folder(input_path, output_zip)
        domain = f"{args.domain_prefix}-{input_path.name}".lower() if args.domain_prefix else None
        upload_to_tiiny(output_zip, domain=domain)
    else:
        print("[❌] input_path non è né un file Markdown né una cartella.")

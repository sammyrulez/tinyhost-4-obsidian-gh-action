# 🌐 Tiiny Markdown Publisher

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/sammyrulez/tinyhost-4-obsidian-gh-action/test-action.yml?branch=main&label=publish&style=flat-square)

A reusable GitHub Action that:

✅ Converts Markdown files (`.md`) to styled HTML using [Pico.css](https://picocss.com)  
📦 Optionally zips multiple `.md` files if a directory is provided  
🚀 Publishes the result on [Tiiny.host](https://tiiny.host) via API  

---

## 📦 What It Does

- Converts one `.md` file → a single HTML page with Pico styling
- Converts all `.md` files in a folder → zipped HTML pages
- Automatically uploads the result to Tiiny.host
- Can generate a domain name based on a prefix and file/folder name

---

## 📥 Inputs

| Name            | Required | Description                                                                 |
|-----------------|----------|-----------------------------------------------------------------------------|
| `input_path`    | ✅ Yes    | Path to a `.md` file or a folder containing `.md` files                     |
| `output_name`   | ❌ No     | Output `.html` or `.zip` filename (optional). Defaults to match input name |
| `tiiny_api_key` | ✅ Yes    | Your [Tiiny.host](https://tiiny.host) API key                              |
| `tiiny_prefix`  | ❌ No     | Prefix for auto-generated domain (e.g., `myproject-filename.tiiny.site`)   |

---

## 🔐 Secrets Setup

In your repository, go to  
`Settings → Secrets and variables → Actions → New repository secret`  
and add the following:

- `TIINY_API_KEY` – your API key from [Tiiny.host](https://tiiny.host)

Optionally, set:
- `TIINY_PREFIX` – a short prefix like `blog`, `demo`, etc.

---

## 🚀 Usage Example

```yaml
name: Publish Markdown to Tiiny.host

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Publish Markdown folder as site
        uses: your-username/tiiny-markdown-action@main
        with:
          input_path: docs
          tiiny_api_key: ${{ secrets.TIINY_API_KEY }}
          tiiny_prefix: blog

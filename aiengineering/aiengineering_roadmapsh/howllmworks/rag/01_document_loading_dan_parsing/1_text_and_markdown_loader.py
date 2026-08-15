import os
import re
import datetime

class Document:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"<Document content_length={len(self.page_content)} metadata={self.metadata}>"

def parse_markdown_frontmatter(content: str):
    """Memisahkan frontmatter YAML (jika ada) dari konten markdown."""
    frontmatter = {}
    body = content

    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        body = content[match.end():]
        for line in yaml_text.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                frontmatter[key.strip()] = val.strip().strip('"\'')
    return body, frontmatter

def load_markdown_file(file_path: str) -> Document:
    """Membaca file Markdown, menarik metadata file & frontmatter."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    body, frontmatter = parse_markdown_frontmatter(raw_content)

    stat = os.stat(file_path)
    metadata = {
        "source": os.path.abspath(file_path),
        "filename": os.path.basename(file_path),
        "file_size_bytes": stat.st_size,
        "created_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "char_count": len(body),
        "word_count": len(body.split()),
        **frontmatter
    }

    return Document(page_content=body.strip(), metadata=metadata)

def main():
    print("=== 01. Document Loading: Text & Markdown Loader ===")

    # Contoh membuat file sampel sementara untuk demo
    sample_md_path = "sample_doc.md"
    sample_content = """---
title: Panduan AI Engineering RAG
author: Bsa
tags: ["ai", "rag", "roadmap"]
---

# Pengenalan RAG

Retrieval-Augmented Generation (RAG) adalah arsitektur yang menggabungkan kemampuan pencarian basis pengetahuan (Retrieval) dengan kemampuan generasi LLM.

## Keuntungan RAG
- Mengurangi halusinasi model.
- Mengakses data privat atau enterprise secara real-time.
- Tidak memerlukan fine-tuning model yang mahal.
"""

    with open(sample_md_path, "w", encoding="utf-8") as f:
        f.write(sample_content)

    doc = load_markdown_file(sample_md_path)

    print(f"\n[OK] Dokumen berhasil di-load:")
    print(f"Content Preview:\n{doc.page_content[:150]}...")
    print("\nMetadata Ter-ekstraksi:")
    for k, v in doc.metadata.items():
        print(f"  - {k}: {v}")

    # Cleanup sample
    if os.path.exists(sample_md_path):
        os.remove(sample_md_path)

if __name__ == "__main__":
    main()

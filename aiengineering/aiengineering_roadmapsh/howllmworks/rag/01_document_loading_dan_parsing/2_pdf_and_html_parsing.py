import re
import html

class HTMLCleanerParser:
    """Parser HTML sederhana untuk membuang tag berisik dan mengekstrak teks bersih."""
    def parse(self, html_content: str) -> str:
        # Membuang tag script & style
        cleaned = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r'<style.*?>.*?</style>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
        # Membuang tag HTML
        cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
        # Decode HTML entities (&amp;, &lt;, dll)
        cleaned = html.unescape(cleaned)
        # Normalkan whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

def parse_pdf_demo(pdf_path: str):
    """Mencoba ekstraksi PDF dengan pypdf jika terinstall, atau menggunakan fallback simulator."""
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            pages.append({"page_number": i + 1, "text": text})
        return pages
    except ImportError:
        print("[INFO] Library 'pypdf' tidak ditemukan. Menggunakan simulator PDF parsing...")
        return [
            {"page_number": 1, "text": "Halaman 1: Pengenalan Sistem Vector Database dan RAG Pipeline."},
            {"page_number": 2, "text": "Halaman 2: Metode chunking dan strategi pencarian hybrid (Dense + Sparse)."}
        ]

def main():
    print("=== 02. Document Parsing: PDF & HTML ===")

    # 1. Demo HTML Parsing
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head><title>AI RAG Tutorial</title><style>body { color: red; }</style></head>
    <body>
        <nav><a href="#">Home</a> | <a href="#">About</a></nav>
        <h1>Arsitektur RAG Scalable</h1>
        <p>Sistem RAG modern menggunakan <strong>Vector Database</strong> seperti ChromaDB atau Qdrant.</p>
        <script>console.log("Analytics tracker");</script>
    </body>
    </html>
    """
    html_parser = HTMLCleanerParser()
    clean_text = html_parser.parse(sample_html)
    print("\n[HTML Parser Result]")
    print(f"Hasil Teks Bersih:\n'{clean_text}'")

    # 2. Demo PDF Parsing
    print("\n[PDF Parser Result]")
    pdf_pages = parse_pdf_demo("non_existent_sample.pdf")
    for page in pdf_pages:
        print(f"  - Page {page['page_number']}: {page['text']}")

if __name__ == "__main__":
    main()

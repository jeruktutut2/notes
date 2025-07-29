use std::{io::Cursor, path::PathBuf};

use anyhow::Ok;
use genpdf::{elements, fonts, Document};
use printpdf::{Mm, Op, PdfDocument, PdfPage, PdfSaveOptions};

pub trait PdfService {
    async fn generate_pdf_from_string(&self) -> Result<Vec<u8>, anyhow::Error>;
    async fn generate_pdf(&self) -> String;
}

pub struct PdfServiceImpl {

}

impl PdfServiceImpl {
    pub fn new() -> PdfServiceImpl {
        PdfServiceImpl {  }
    }
}

impl PdfService for PdfServiceImpl {
    async fn generate_pdf_from_string(&self) -> Result<Vec<u8>, anyhow::Error> {
        // let font_family = genpdf::fonts::from_files("../fonts", "OpenSans", None)?;
        let font_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("src/fonts");
        let font_str_dir = font_dir.to_str().unwrap();
        let font_family = fonts::from_files(font_str_dir, "Roboto", None)?;
        let mut document = Document::new(font_family);
        document.set_title("title");

        let mut decorator = genpdf::SimplePageDecorator::new();
        decorator.set_margins(10);
        document.set_page_decorator(decorator);

        let paragraph = elements::Paragraph::new("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
            .aligned(genpdf::Alignment::Left);
        document.push(paragraph);

        let mut buffer = Cursor::new(Vec::new());
        document.render(&mut buffer)?;
        Ok(buffer.into_inner())
    }

    async fn generate_pdf(&self) -> String {
        let mut doc = PdfDocument::new("My first PDF");
        let page1_contents = vec![Op::Marker { id: "debugging-marker".to_string() }];
        let page1 = PdfPage::new(Mm(10.0), Mm(250.0), page1_contents);
        let pdf_bytes: Vec<u8> = doc
            .with_pages(vec![page1])
            .save( &PdfSaveOptions::default());
        return "success".to_string();
    }
}
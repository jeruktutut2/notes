use std::io::Cursor;

use base64::{engine::general_purpose, Engine};
use image::ImageReader;

use crate::models::requests::image_request::ImageRequest;

pub trait ImageService {
    async fn check_image(&self, image_request: ImageRequest) -> String;
}

pub struct ImageServiceImpl {}

impl ImageServiceImpl {
    pub fn new() -> ImageServiceImpl {
        ImageServiceImpl {}
    }
}

impl ImageService for ImageServiceImpl {
    async fn check_image(&self, image_request: ImageRequest) -> String {
        let image_decoded = match general_purpose::STANDARD.decode(image_request.image) {
            Ok(image_decoded) => image_decoded,
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string()
            }
        };
        let has_magic_bytes = image_decoded.starts_with(b"\xFF\xD8\xFF") // JPEG
            || image_decoded.starts_with(b"\x89PNG\r\n\x1A\n") // PNG
            || image_decoded.starts_with(b"GIF87a") || image_decoded.starts_with(b"GIF89a"); // GIF
        if !has_magic_bytes {
            return "error has no magic bytes".to_string()
        }

        let image_cursor = Cursor::new(image_decoded);
        let is_image = ImageReader::new(image_cursor).with_guessed_format().is_ok();
        if !is_image {
            return "is not image".to_string()
        }
        "ok".to_string()
    }
}
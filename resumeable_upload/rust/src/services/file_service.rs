use std::{fs::{self, OpenOptions}, io::Write, path::PathBuf};

use bytes::Bytes;
use futures::StreamExt;
use regex::Regex;
use tokio::{fs::File, io::{AsyncReadExt, AsyncWriteExt}};
use tokio_stream::wrappers::ReadDirStream;

pub trait FileService {
    async fn upload(&self, file_id: &str, chunk_index: &str, chunk: Bytes) -> String;
    async fn merge(&self, file_id: &str, total_chunks: &str) -> String;
    async fn check_file(&self, file_id: &str) -> (Vec<usize>, String);
    async fn upload_and_merge(&self, file_id: String, chunk_index: String, last_chunk_index: String, chunk: Bytes) -> String;
}

pub struct FileServiceImpl {}

impl FileServiceImpl {
    pub fn new() -> FileServiceImpl {
        FileServiceImpl {  }
    }
}

impl FileService for FileServiceImpl {
    async fn upload(&self, file_id: &str, chunk_index: &str, chunk: Bytes) -> String {
        let upload_dir = PathBuf::from("uploads");
        fs::create_dir_all(&upload_dir).unwrap();
        let part_path = upload_dir.join(format!("{}.part{}", file_id, chunk_index));
        let mut file = match OpenOptions::new().create(true).write(true).open(part_path) {
            Ok(file) => file,
            Err(err) => {
                println!("error: {}", err);
                return err.to_string();
            }
        };
        match file.write_all(&chunk) {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return err.to_string();
            }
        };
        "success".to_string()
    }

    async fn merge(&self, file_id: &str, total_chunks: &str) -> String {
        let mut files: Vec<(usize, PathBuf)> = Vec::new();
        let pattern = Regex::new(&format!(r"^{}\.part(\d+)$", regex::escape(file_id))).unwrap();
        let read_dir = match tokio::fs::read_dir("uploads").await {
            Ok(r) => r,
            Err(err) => return err.to_string(),
        };
        let mut dir_stream = ReadDirStream::new(read_dir);

        while let Some(Ok(entry)) = dir_stream.next().await {
            let file_name = entry.file_name().to_string_lossy().to_string();
            if let Some(captures) = pattern.captures(&file_name) {
                if let Some(m) = captures.get(1) {
                    if let Ok(index) = m.as_str().parse::<usize>() {
                        files.push((index, entry.path()));
                    }
                }

            }
        }
        files.sort_by_key(|(index, _)| *index);
        let mut output_file = match File::create("uploads/file_upload.merged").await {
            Ok(output_file) => output_file,
            Err(err) => {
                println!("error: {}", err);
                return err.to_string();
            }
        };
        for (_, part_path) in files {
            let mut part_file = match File::open(&part_path).await {
                Ok(part_file) => part_file,
                Err(err) => {
                    println!("error: {}", err);
                    return err.to_string();
                }
            };
            let mut buffer = Vec::new();
            match part_file.read_to_end(&mut buffer).await {
                Ok(_) => (),
                Err(err) => {
                    println!("error: {}", err);
                    return err.to_string();
                }
            };
            match output_file.write_all(&buffer).await {
                Ok(_) => (),
                Err(err) => {
                    println!("error: {}", err);
                    return err.to_string();
                }
            }
            
            match tokio::fs::remove_file(&part_path).await {
                Ok(_) => (),
                Err(err) => {
                    println!("error: {}", err);
                    return err.to_string();
                }
            }
        }

        let data = match tokio::fs::read("uploads/file_upload.merged").await {
            Ok(data) => data,
            Err(err) => {
                println!("error: {}", err);
                return err.to_string();
            }
        };
        let info = match infer::get(&data) {
            Some(info) => {
                match tokio::fs::rename("uploads/file_upload.merged", format!("{}.{}", "uploads/file_upload", info.extension())).await {
                    Ok(_) => (),
                    Err(err) => {
                        println!("error: {}", err);
                        return err.to_string();
                    }
                };
            },
            None => {
                println!("cannot get extention output file");
                return "cannot get extention output file".to_string();
            }
        };
        "success".to_string()
    }

    async fn check_file(&self, file_id: &str) -> (Vec<usize>, String) {
        let mut files: Vec<(usize, PathBuf)> = Vec::new();
        let pattern = Regex::new(&format!(r"^{}\.part(\d+)$", regex::escape(file_id))).unwrap();
        let read_dir = match tokio::fs::read_dir("uploads").await {
            Ok(r) => r,
            Err(err) => return (vec![], err.to_string()),
        };
        let mut dir_stream = ReadDirStream::new(read_dir);
        while let Some(Ok(entry)) = dir_stream.next().await {
            let file_name = entry.file_name().to_string_lossy().to_string();
            if let Some(captures) = pattern.captures(&file_name) {
                if let Some(m) = captures.get(1) {
                    if let Ok(index) = m.as_str().parse::<usize>() {
                        files.push((index, entry.path()));
                    }
                }

            }
        }
        files.sort_by_key(|(index, _)| *index);
        let mut indices: Vec<usize> = vec![];
        for (index, _s) in files {
            indices.push(index);
        };
        return (indices, "success".to_string())
    }

    async fn upload_and_merge(&self, file_id: String, chunk_index: String, last_chunk_index: String, chunk: Bytes) -> String {
        let mut output_file = match tokio::fs::OpenOptions::new().create(true).append(true).open("uploads/file_upload.merged").await {
            Ok(output_file) => output_file,
            Err(err) => {
                println!("error: {}", err);
                return err.to_string();
            }
        };
        match output_file.write_all(&chunk).await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return err.to_string();
            }
        };

        if chunk_index == last_chunk_index {
            let data = match tokio::fs::read("uploads/file_upload.merged").await {
                Ok(data) => data,
                Err(err) => {
                    println!("error: {}", err);
                    return err.to_string();
                }
            };
            let info = match infer::get(&data) {
                Some(info) => {
                    match tokio::fs::rename("uploads/file_upload.merged", format!("{}.{}", "uploads/file_upload", info.extension())).await {
                        Ok(_) => (),
                        Err(err) => {
                            println!("error: {}", err);
                            return err.to_string();
                        }
                    };
                },
                None => {
                    println!("cannot get extention output file");
                    return "cannot get extention output file".to_string();
                }
            };
        }
        "success".to_string()
    }
}
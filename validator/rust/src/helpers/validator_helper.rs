use std::collections::HashMap;
use validator::{ValidationError, ValidationErrors};
use regex::Regex;

pub fn get_validation_error(errors: ValidationErrors) -> HashMap<String, String> {
    let mut error_message = HashMap::new();
    for (field, errors) in errors.field_errors() {
        for error in errors {
            match error_message.get(&field.clone().to_string()) {
                Some(value) => {
                    error_message.insert(field.clone().to_string(), format!("{}, {}", value, error));
                }
                None => {
                    error_message.insert(field.clone().to_string(), error.to_string());
                }
            }
        }
    }
    error_message
}

pub fn validate_password(password: &str) -> Result<(), ValidationError> {
    let mut errors: Vec<String> = vec![];

    let is_length_equal_or_more_then_8 = password.len() >= 8;
    if !is_length_equal_or_more_then_8 {
        errors.push("password must consists at least 8 characters".to_string());
    }

    let has_number = Regex::new(r"\d").unwrap().is_match(password);
    if !has_number {
        errors.push("password must consists at least 1 number".to_string());
    }

    let has_lowercase = Regex::new(r"[a-z]").unwrap().is_match(password);
    if !has_lowercase {
        errors.push("password must consists at least 1 lowercase".to_string());
    }

    let has_uppercase = Regex::new(r"[A-Z]").unwrap().is_match(password);
    if !has_uppercase {
        errors.push("password must consists at least 1 uppercase".to_string());
    }

    let has_special_character = Regex::new("r[!@#$%^&*(),.?\":{}|<>]").unwrap().is_match(password);
    if !has_special_character {
        errors.push("password must consists at least 1 special character".to_string());
    }

    if errors.is_empty() {
        return Ok(());
    } else {
       let mut error = ValidationError::new("invalid validate password"); 
       error.message = Some(errors.join(",").into());
       return Err(error);
    }
}
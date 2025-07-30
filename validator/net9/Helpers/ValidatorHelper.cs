using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Mvc.ModelBinding;

namespace net9.Helpers;

public static class ValidatorHelper
{
    public static Dictionary<String, String> Validate(ModelStateDictionary ModelState, Type type)
    {
        Dictionary<String, String> errors = [];
        foreach (var state in ModelState) {
            string key = state.Key;
            
            foreach (var error in state.Value.Errors) {
                var property = type.GetProperty(key);
                var jsonAttr = property.GetCustomAttributes(typeof(JsonPropertyNameAttribute), false).FirstOrDefault() as JsonPropertyNameAttribute;
                string field = jsonAttr?.Name ?? key;
                errors.Add(field, error.ErrorMessage);
            }
        }
        return errors;
    }
}
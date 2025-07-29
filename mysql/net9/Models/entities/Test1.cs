using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

[Table("test1")]
public class Test1
{
    [JsonPropertyName("id")]
    [Key]
    [Column("id")]
    public int Id { set; get; }

    [JsonPropertyName("test")]
    [Required]
    [Column("test")]
    public required string Test { set; get; }
}
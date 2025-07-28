using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace net9.Models.Entities;

[Table("test1")]
public class Test1
{
    [Key]
    [Column("id")]
    public required Guid Id { set; get; }

    [Required]
    [Column("test")]
    public required string Test { set; get; }
}